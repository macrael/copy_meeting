Copy Meeting

This script generates a `scheduled meeting` from the Zoom API and prints out the join url.

I have configured this as a macOS Service so that I can invoke it with a key-combo and have the result copied to the pasteboard.

Configuration
-------------------

1. create a "server to server" zoom app in the developer portal
	* add the Meetings: Create Meeting permission scope to it
2. create a `zoom_creds` file in this directory that looks like this:

```
account_id=[ACCOUNT ID]
client_id=[CLIENT ID]
client_secret=[CLIENT SECRET]
```

3. run `pipenv install`
4. run `pipenv shell`
5. run `mypy copy_meeting.py && ./copy_meeting.py`

Use Automator to create a new Quick Action to make a Service.
Or, use keyboard maestro.
