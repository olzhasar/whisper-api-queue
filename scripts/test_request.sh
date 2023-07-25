#!/bin/bash

if [ -z $1 ] ; then
  echo "Provide a path to the input mp3 file" && exit 1;
fi

MEDIA_DIR=./media

cp $1 ${MEDIA_DIR}

filename=$(basename $1)

curl -X POST http://localhost:8000 -H "Content-Type: application/json" -d '{"file_url": "http://dummy/media/'${filename}'", "webhook_url": "http://dummy"}'
