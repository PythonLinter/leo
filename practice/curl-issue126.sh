#!/usr/bin/env bash

shopt -s expand_aliases


HOST="nc.carrene.com"
#USERNAME="begocivixo@lilylee.com"
USERNAME="hamed@carrene.com"
PASSWORD="123456"
TOKEN_REGEX="[[:space:][:alnum:]\.=:;,//_-]*"
REFRESH_TOKEN=""
TOKEN=""

RESP=`curl -D- -s ${HOST}/apiv1/sessions -F"email=${USERNAME}" -F"password=${PASSWORD}"`
while read -r line
do
    if [[ $line =~ ^Set-Cookie:[[:space:]](refresh-token=${TOKEN_REGEX}) ]]; then
        REFRESH_TOKEN=$(echo ${BASH_REMATCH[1]}|tr -d '\r')
    elif [[ $line =~ ^[[:blank:]]*\"token\":\"(${TOKEN_REGEX}) ]]; then
        TOKEN="${BASH_REMATCH[1]}"
    fi
done <<< "$RESP"
echo "Refresh Token: ${REFRESH_TOKEN}"
echo "Token: ${TOKEN}"


# This your token
TOKEN="eyJleHAiOjE0OTM5MjE2MjUsImlhdCI6MTQ5MzkyMTU2NSwiYWxnIjoiSFMyNTYifQ.eyJlbWFpbCI6ImVoc2FuQGNhcnJlbmUuY29tIiwiaWQiOjYsInNlc3Npb25JZCI6IjAxMzdlM2ExLWUwZmQtNDFiZi05MzAzLTNhYjc4YjJjODk0ZCIsInJvbGVzIjpbInVzZXIiXX0.rJqqcOsy_ylCm3zOhR1nsagZ0hdKQBNrfntrd0rWn7I"

alias curl="curl -ss -H\"Authorization: Bearer ${TOKEN}\" -H \"Cookie: $REFRESH_TOKEN\" $@"

echo "AUTH DONE"
curl ${HOST}/apiv1/codes?specialityId=2
