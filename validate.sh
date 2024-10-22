#!/bin/bash

API_URL="http://localhost:8000/users?page=1&page_size=2000"

# Make the API call and capture the response
response=$(curl -s $API_URL)

# Validate the response body structure using grep and awk
if echo "$response" | grep -q '"page_number"' && \
   echo "$response" | grep -q '"page_size"' && \
   echo "$response" | grep -q '"total_count"' && \
   echo "$response" | grep -q '2000' && \
   echo "$response" | grep -q '"users"' && \
   echo "$response" | awk '/"users": \[/ {flag=1; next} /]/ {flag=0} flag {print}' | grep -q '.'; then
  echo "Response body is valid."
else
  echo "Response body is invalid."
fi
