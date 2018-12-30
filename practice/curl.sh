#!/usr/bin/env bash

shopt -s expand_aliases


HOST="https://nc.carrene.com"
#HOST="http://localhost:8080"
#USERNAME="begocivixo@lilylee.com"
USERNAME="hamed@carrene.com"
#USERNAME="user1@example.com"
PASSWORD="123456"
TOKEN_REGEX="[[:space:][:alnum:]\.=:;,//_-]*"
REFRESH_TOKEN=""
TOKEN=""

RESP=`curl -ss -D- ${HOST}/apiv1/sessions -F"email=${USERNAME}" -F"password=${PASSWORD}"`
while read -r line
do
    if [[ $line =~ ^Set-Cookie:[[:space:]](refresh-token=${TOKEN_REGEX}) ]]; then
        REFRESH_TOKEN=$(echo ${BASH_REMATCH[1]}|tr -d '\r')
    elif [[ $line =~ ^[[:blank:]]*\"token\":\"(${TOKEN_REGEX}) ]]; then
        TOKEN="${BASH_REMATCH[1]}"
    fi
done <<< "$RESP"
#REFRESH_TOKEN=`python -c "print('$REFRESH_TOKEN'.split(';')[0])"`
echo "Refresh Token: ${REFRESH_TOKEN}"
echo "Token: ${TOKEN}"
alias curl="curl -ss -H\"Authorization: Bearer ${TOKEN}\" -H \"Cookie: ${REFRESH_TOKEN}\" $@"

echo "AUTH DONE"

sleep 4
curl -D- ${HOST}/apiv1/codes?take=10&skip=20
#curl -XPOST ${HOST}/apiv1/collections/50 -F"codeId=9"
#curl ${HOST}/apiv1/collections
#curl ${HOST}/apiv1/codes?specialityId=1 
#echo
