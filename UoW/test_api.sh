#!/bin/bash

# Test script for Access Request Management API
# Uses httpie for HTTP requests
# Make sure the server is running before executing this script

set -e  # Exit on error

API_URL="http://127.0.0.1:8000"

echo "=========================================="
echo "Testing Access Request Management API"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Creating first access request with 2 approvers${NC}"
echo "---"
RESPONSE=$(http -vv POST ${API_URL}/access-requests/ \
  requester="john.doe@example.com" \
  resource="Production Database" \
  approvers:='[
    {"name": "Alice Smith", "email": "alice@example.com"},
    {"name": "Bob Johnson", "email": "bob@example.com"}
  ]')

echo "$RESPONSE"
REQUEST_ID_1=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo -e "${GREEN}✓ Created access request with ID: $REQUEST_ID_1${NC}"
echo ""

echo -e "${BLUE}2. Listing all access requests${NC}"
echo "---"
http -vv GET ${API_URL}/access-requests/
echo -e "${GREEN}✓ Listed all access requests${NC}"
echo ""

echo -e "${BLUE}3. Getting specific access request (ID: $REQUEST_ID_1)${NC}"
echo "---"
http -vv GET ${API_URL}/access-requests/${REQUEST_ID_1}
echo -e "${GREEN}✓ Retrieved access request $REQUEST_ID_1${NC}"
echo ""

echo -e "${BLUE}4. First approval - Alice approves request $REQUEST_ID_1${NC}"
echo "---"
http -vv POST ${API_URL}/access-requests/${REQUEST_ID_1}/approve \
  approver_email="alice@example.com"
echo -e "${GREEN}✓ Alice approved the request (status should still be PENDING)${NC}"
echo ""

echo -e "${BLUE}5. Second approval - Bob approves request $REQUEST_ID_1${NC}"
echo "---"
http -vv POST ${API_URL}/access-requests/${REQUEST_ID_1}/approve \
  approver_email="bob@example.com"
echo -e "${GREEN}✓ Bob approved the request (status should now be APPROVED)${NC}"
echo ""

echo -e "${BLUE}6. Creating second access request${NC}"
echo "---"
http -vv POST ${API_URL}/access-requests/ \
  requester="jane.smith@example.com" \
  resource="AWS Production Account" \
  approvers:='[
    {"name": "Charlie Brown", "email": "charlie@example.com"},
    {"name": "Diana Prince", "email": "diana@example.com"}
  ]'

REQUEST_ID_2=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo -e "${GREEN}✓ Created access request with ID: $REQUEST_ID_2${NC}"
echo ""

echo -e "${BLUE}7. Denying request $REQUEST_ID_2 - Charlie denies${NC}"
echo "---"
http -vv POST ${API_URL}/access-requests/${REQUEST_ID_2}/deny \
  approver_email="charlie@example.com"
echo -e "${GREEN}✓ Charlie denied the request (status should now be DENIED)${NC}"
echo ""

echo -e "${BLUE}8. Listing all access requests (should show 2 requests)${NC}"
echo "---"
http -vv GET ${API_URL}/access-requests/
echo -e "${GREEN}✓ Listed all access requests${NC}"
echo ""

echo -e "${BLUE}9. Listing only APPROVED requests${NC}"
echo "---"
http -vv GET "${API_URL}/access-requests/?status_filter=APPROVED"
echo -e "${GREEN}✓ Listed APPROVED requests${NC}"
echo ""

echo -e "${BLUE}10. Listing only DENIED requests${NC}"
echo "---"
http -vv GET "${API_URL}/access-requests/?status_filter=DENIED"
echo -e "${GREEN}✓ Listed DENIED requests${NC}"
echo ""

echo -e "${BLUE}11. Listing only PENDING requests${NC}"
echo "---"
http -vv GET "${API_URL}/access-requests/?status_filter=PENDING"
echo -e "${GREEN}✓ Listed PENDING requests${NC}"
echo ""

echo -e "${YELLOW}Testing error cases...${NC}"
echo ""

echo -e "${BLUE}12. Try to create request with only 1 approver (should fail)${NC}"
echo "---"
http -vv POST ${API_URL}/access-requests/ \
  requester="test@example.com" \
  resource="Test Resource" \
  approvers:='[{"name": "Test User", "email": "test@example.com"}]' \
  || echo -e "${GREEN}✓ Correctly rejected request with only 1 approver${NC}"
echo ""

echo -e "${BLUE}13. Try to approve with wrong email (should fail)${NC}"
echo "---"
http -vv POST ${API_URL}/access-requests/${REQUEST_ID_1}/approve \
  approver_email="wrong@example.com" \
  || echo -e "${GREEN}✓ Correctly rejected approval from non-approver${NC}"
echo ""

echo -e "${BLUE}14. Try to approve already finalized request (should fail)${NC}"
echo "---"
http -vv POST ${API_URL}/access-requests/${REQUEST_ID_1}/approve \
  approver_email="alice@example.com" \
  || echo -e "${GREEN}✓ Correctly rejected approval of already finalized request${NC}"
echo ""

echo -e "${BLUE}15. Try to get non-existent request (should fail)${NC}"
echo "---"
http -vv GET ${API_URL}/access-requests/99999 \
  || echo -e "${GREEN}✓ Correctly returned 404 for non-existent request${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}All tests completed!${NC}"
echo "=========================================="
