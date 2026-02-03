import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import email
import json
from typing import List, Optional

class EmailConfig(BaseModel):
    smtp_server: str = Field(description="SMTP server address")
    smtp_port: int = Field(default=587, description="SMTP server port")
    email_address: EmailStr = Field(description="Email address for sending/receiving")
    password: str = Field(description="Email password or app password")
    imap_server: str = Field(description="IMAP server address")

class SendEmailRequest(BaseModel):
    to: List[EmailStr] = Field(description="Recipients' email addresses")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body content")
    cc: List[EmailStr] = Field(default=[], description="CC recipients")
    bcc: List[EmailStr] = Field(default=[], description="BCC recipients")
    attachments: List[str] = Field(default=[], description="File paths to attach")

class ReadEmailsRequest(BaseModel):
    folder: str = Field(default="INBOX", description="Mail folder to read from")
    limit: int = Field(default=10, description="Maximum number of emails to return")
    unread_only: bool = Field(default=False, description="Only return unread emails")

class EmailMCP:
    def __init__(self):
        self.app = FastMCP("email")
        self.config = None
        
    def set_config(self, config: EmailConfig):
        self.config = config

    async def send_email(self, to: List[str], subject: str, body: str, 
                         cc: List[str] = [], bcc: List[str] = [], 
                         attachments: List[str] = []) -> dict:
        """Send an email with optional attachments."""
        if not self.config:
            return {"success": False, "error": "Email configuration not set"}
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.email_address
            msg['To'] = ', '.join(to)
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            for file_path in attachments:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_path.split("/")[-1]}'
                    )
                    msg.attach(part)
            
            # Connect to server and send email
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            server.login(self.config.email_address, self.config.password)
            
            all_recipients = to + cc + bcc
            text = msg.as_string()
            server.sendmail(self.config.email_address, all_recipients, text)
            server.quit()
            
            return {
                "success": True,
                "message": f"Email sent to {len(to)} recipients"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def read_emails(self, folder: str = "INBOX", limit: int = 10, 
                          unread_only: bool = False) -> dict:
        """Read emails from specified folder."""
        if not self.config:
            return {"success": False, "error": "Email configuration not set"}
        
        try:
            mail = imaplib.IMAP4_SSL(self.config.imap_server)
            mail.login(self.config.email_address, self.config.password)
            mail.select(folder)
            
            # Search criteria
            search_criteria = "(UNSEEN)" if unread_only else "ALL"
            status, messages = mail.search(None, search_criteria)
            
            email_ids = messages[0].split()
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            emails = []
            for e_id in reversed(email_ids):  # Reverse to get newest first
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                
                email_info = {
                    "id": e_id.decode(),
                    "subject": msg.get("Subject", ""),
                    "from": msg.get("From", ""),
                    "date": msg.get("Date", ""),
                    "body": ""
                }
                
                # Extract body
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            email_info["body"] = part.get_payload(decode=True).decode()
                            break
                else:
                    email_info["body"] = msg.get_payload(decode=True).decode()
                
                emails.append(email_info)
            
            mail.close()
            mail.logout()
            
            return {
                "success": True,
                "emails": emails,
                "count": len(emails)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def create_email_server():
    server = EmailMCP()
    
    @server.app.tool("send_email", "Send an email with optional attachments")
    async def handle_send_email(req: SendEmailRequest) -> dict:
        return await server.send_email(
            req.to, req.subject, req.body, 
            req.cc, req.bcc, req.attachments
        )
    
    @server.app.tool("read_emails", "Read emails from specified folder")
    async def handle_read_emails(req: ReadEmailsRequest) -> dict:
        return await server.read_emails(req.folder, req.limit, req.unread_only)
    
    return server

if __name__ == "__main__":
    import uvicorn
    server = create_email_server()
    
    # Example configuration (replace with real credentials)
    config = EmailConfig(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        email_address="your_email@gmail.com",
        password="your_app_password",
        imap_server="imap.gmail.com"
    )
    server.set_config(config)
    
    async def run_server():
        config_obj = uvicorn.Config(app=server.app, host="127.0.0.1", port=3002)
        server_instance = uvicorn.Server(config_obj)
        await server_instance.serve()
    
    asyncio.run(run_server())