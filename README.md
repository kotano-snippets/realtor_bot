# realtor_bot
Telegram realtor bot


## Launching tests
To launch tests run pytest in the project's root directory
```
rootdir$ pytest
```

To run tests successfully you need to start conversation with bot in telegram.

You can set bot credentials manually in test file or use existing by subscribing to bot username described in `testbot_username` variable.
After that put your chat id into a `test_id` variable to see the test results.