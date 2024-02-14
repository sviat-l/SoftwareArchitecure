#curl -X POST -H "Content-Type: application/json" -d '{"msg": "message2"}' http://localhost:4200/send

curl http://localhost:4200/get_messages -H "Content-Type: application/json"
#{"logging_responce":"","messages_responce":"not implemented yet"}
curl -X POST -H "Content-Type: application/json" -d '{"msg": "APZ is cool"}' http://localhost:4200/send
#{"status":"success"}
curl http://localhost:4200/get_messages -H "Content-Type: application/json"
#{"logging_responce":"APZ is cool","messages_responce":"not implemented yet"}
curl -X POST -H "Content-Type: application/json" -d '{"msg": "Another message"}' http://localhost:4200/send
#{"status":"success"}
curl -X POST -H "Content-Type: application/json" -d '{"msg": "One more message"}' http://localhost:4200/send
#{"status":"success"}
curl http://localhost:4200/get_messages -H "Content-Type: application/json"
#{"logging_responce":"APZ is cool\n|Another message","messages_responce":"not implemented yet"}
curl -X POST -H "Content-Type: application/json" -d '{"msg": "Final logging message"}' http://localhost:4200/send
#{"status":"success"}
curl http://localhost:4200/get_messages -H "Content-Type: application/json"
#{"logging_responce":"APZ is cool\n|Another message\n|One more message\n|Final logging message","messages_responce":"not implemented yet"}

