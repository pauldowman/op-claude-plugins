#!/bin/bash

# Script to list all values for stack.optimism.io/network from the k8s repo
# Usage: ./scripts/list_network_values.sh <path to k8s repo>

set -euo pipefail

# Function to print output
print_header() {
    echo "=== $1 ==="
}

print_info() {
    echo -e "$1"
}

print_error() {
    echo "Error: $1" >&2
}

if [ -z "$1" ]; then
    print_error "Please provide the path to the k8s repository"
    exit 1
fi

cd "$1"

# Check if opc directory exists
if [ ! -d "opc" ]; then
    print_error "opc directory not found in current directory"
    echo "Please run this script from the root of the k8s repository"
    exit 1
fi

# Use grep to find all occurrences and extract the values
network_values=$(find opc -type f \( -name "*.yaml" -o -name "*.yml" \) -exec grep -l "stack\.optimism\.io/network" {} \; | \
    xargs grep "stack\.optimism\.io/network:" | \
    sed 's/.*stack\.optimism\.io\/network:[[:space:]]*//' | \
    sort | uniq)

if [ -z "$network_values" ]; then
    print_error "No stack.optimism.io/network values found"
    exit 1
fi

# Count total values
total_count=$(echo "$network_values" | wc -l)

# Categorize by suffix
dev_count=$(echo "$network_values" | grep -c "\-dev$" || true)
prod_count=$(echo "$network_values" | grep -c "\-prod$" || true)
other_count=$((total_count - dev_count - prod_count))

echo "Development environments (-dev): $dev_count"
echo "Production environments (-prod): $prod_count"
echo "Other environments: $other_count"

print_info "\nDevelopment environments:"
echo "$network_values" | grep "\-dev$" | sed 's/^/  /'

print_info "\nProduction environments:"
echo "$network_values" | grep "\-prod$" | sed 's/^/  /'

if [ $other_count -gt 0 ]; then
    print_info "\nOther environments:"
    echo "$network_values" | grep -v "\-dev$" | grep -v "\-prod$" | sed 's/^/  /'
fi
