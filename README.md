# fb_reply
## Feature
Use selenium to control web UI. If there is new message, the bot will reply to it with predetermined message.

## Known issues
1. depends on the messenger web UI DOM. Code may fail if the UI changes
2. no reply to active diagloue (currenly opened chatbox). new message coming from that use will not induce any <b>new message</b> notification

## Future improvments
messenger use websocket for communication. Ideally we should use libraries like urllib3 to manage the websockets instead of using the messenger web UI, by which we can get rid of the problems...
