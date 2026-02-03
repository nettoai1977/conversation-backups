#!/bin/bash

# Enhanced CLI Integration Tools for OpenClaw
# Implements the CLI tools enhancement strategies from the research

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
LOG_FILE="/tmp/openclaw_cli_integration.log"
MAX_EXECUTION_TIME=300  # 5 minutes max execution time
SECURITY_MODE="strict"  # strict, moderate, relaxed

# Logging function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Enhanced command execution with security controls
run_enhanced_command() {
    local command="$1"
    local description="${2:-No description provided}"
    local timeout="${3:-30}"
    local allowlist_file="${4:-}"
    
    echo "Executing: $command"
    echo "Description: $description"
    log_message "EXECUTING: $command (Description: $description)"
    
    # Security validation
    if ! validate_command_security "$command"; then
        echo "ERROR: Command failed security validation"
        log_message "SECURITY VIOLATION: $command was blocked"
        return 1
    fi
    
    # Check allowlist if provided
    if [[ -n "$allowlist_file" && -f "$allowlist_file" ]]; then
        if ! check_allowlist "$command" "$allowlist_file"; then
            echo "ERROR: Command not in allowlist"
            log_message "ALLOWLIST VIOLATION: $command was blocked"
            return 1
        fi
    fi
    
    # Execute with timeout and capture output
    local start_time=$(date +%s)
    local result
    result=$(timeout "$timeout" bash -c "$command" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s)
    
    echo "Execution time: $((end_time - start_time)) seconds"
    echo "Exit code: $exit_code"
    
    if [ $exit_code -eq 0 ]; then
        echo "Status: SUCCESS"
        echo "Output:"
        echo "$result"
        log_message "SUCCESS: $command executed in $((end_time - start_time))s"
    else
        echo "Status: FAILED (exit code: $exit_code)"
        echo "Error output:"
        echo "$result"
        log_message "FAILED: $command failed with exit code $exit_code"
    fi
    
    return $exit_code
}

# Security validation function
validate_command_security() {
    local cmd="$1"
    
    # Block dangerous patterns
    local dangerous_patterns=(
        ';\s*&'      # Command chaining
        '&&'         # Logical AND
        '||'         # Logical OR
        '|'          # Pipe operator
        '`'          # Command substitution
        '\$\(.*\)'   # Dollar parentheses
        '/dev/null'  # Redirect to null (potential data hiding)
        '>/dev/'     # Output redirect to device
        '</dev/'     # Input redirect from device
        '>/proc/'    # Writing to proc filesystem
        '<&'         # Input redirection
        '>&'         # Output redirection
    )
    
    for pattern in "${dangerous_patterns[@]}"; do
        if [[ $cmd =~ $pattern ]]; then
            echo "Blocked pattern found: $pattern"
            return 1
        fi
    done
    
    return 0
}

# Check command against allowlist
check_allowlist() {
    local cmd="$1"
    local allowlist_file="$2"
    
    # Extract command name (first word)
    local cmd_name
    cmd_name=$(echo "$cmd" | awk '{print $1}' | xargs basename)
    
    if grep -q "^${cmd_name}$" "$allowlist_file"; then
        return 0
    else
        return 1
    fi
}

# Create allowlist file if it doesn't exist
create_allowlist() {
    local allowlist_file="$1"
    if [[ ! -f "$allowlist_file" ]]; then
        cat > "$allowlist_file" << 'EOF'
# OpenClaw CLI Allowlist
# Add approved commands here, one per line
ls
pwd
whoami
date
echo
cat
grep
find
ps
top
df
du
curl
wget
ping
dig
nslookup
git
docker
npm
yarn
python
python3
node
bash
sh
zsh
EOF
        echo "Created allowlist file: $allowlist_file"
    fi
}

# System monitoring functions
get_system_stats() {
    echo "=== System Statistics ==="
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
    echo "Memory Usage:"
    free -h | grep "Mem:" | awk '{print $3"/"$2" ("$3/$2*100"% used)"}'
    echo "Disk Usage:"
    df -h | grep -E '^/dev/' | awk '{print $5" full on "$6}'
    echo "Uptime:"
    uptime
}

# Process management functions
list_processes() {
    local filter="${1:-.*}"
    echo "=== Processes ($filter) ==="
    ps aux | grep -E "$filter" | grep -v grep
}

# Network connectivity functions
check_connectivity() {
    local host="${1:-google.com}"
    local port="${2:-80}"
    local timeout="${3:-5}"
    
    echo "Checking connectivity to $host:$port (timeout: ${timeout}s)..."
    
    if nc -z -w "$timeout" "$host" "$port"; then
        echo "✓ Connected to $host:$port"
        return 0
    else
        echo "✗ Cannot connect to $host:$port"
        return 1
    fi
}

# File operations functions
search_files() {
    local directory="${1:-.}"
    local pattern="${2:-*.txt}"
    local recursive="${3:-true}"
    
    echo "Searching for files matching '$pattern' in '$directory'..."
    
    if [[ "$recursive" == "true" ]]; then
        find "$directory" -name "$pattern" -type f
    else
        find "$directory" -maxdepth 1 -name "$pattern" -type f
    fi
}

# Main execution starts here
case "${1:-help}" in
    "run")
        # Execute a command with security controls
        if [[ $# -lt 2 ]]; then
            echo "Usage: $0 run <command> [description] [timeout] [allowlist_file]"
            exit 1
        fi
        create_allowlist "/tmp/openclaw_allowlist.txt"
        run_enhanced_command "$2" "${3:-Command executed via OpenClaw}" "${4:-30}" "/tmp/openclaw_allowlist.txt"
        ;;
    
    "monitor")
        # Get system monitoring information
        get_system_stats
        ;;
    
    "processes")
        # List processes with optional filter
        list_processes "${2:-.*}"
        ;;
    
    "connectivity")
        # Check network connectivity
        check_connectivity "${2:-google.com}" "${3:-80}" "${4:-5}"
        ;;
    
    "search")
        # Search for files
        search_files "${2:-.}" "${3:-*.txt}" "${4:-true}"
        ;;
    
    "create-allowlist")
        # Create a default allowlist
        create_allowlist "${2:-./allowlist.txt}"
        echo "Allowlist created at ${2:-./allowlist.txt}"
        ;;
    
    "help"|*)
        echo "OpenClaw Enhanced CLI Integration Tool"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  run <command> [desc] [timeout] [allowlist] - Execute command securely"
        echo "  monitor                                    - Get system statistics"
        echo "  processes [filter]                         - List processes"
        echo "  connectivity [host] [port] [timeout]       - Check connectivity"
        echo "  search [dir] [pattern] [recursive]         - Search for files"
        echo "  create-allowlist [file]                    - Create allowlist"
        echo "  help                                       - Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 run 'ls -la' 'List directory contents'"
        echo "  $0 monitor"
        echo "  $0 processes docker"
        echo "  $0 connectivity github.com 443"
        ;;
esac