# Retriever for RPAN
### Stream on the Reddit Public Access Network straight from your PC - it's simple and hustle-free

Wanna take your RPAN broadcasts to the next level? This is the app you've been looking for! It sets up a stream for you and retrieves the key to it. Pair it with any streaming software and you're good to go - it's really easy to use and completely free.

## FAQ
#### Is this a virus?
No, you've gotta trust me on this one. Or, if you have the knowledge, just check the code and see for yourself - the project is completely open-source ;)
#### Will Retriever have access to my reddit account?
Yes, but don't worry - it only needs it to create a broadcast for you. It does so by asking Reddit for an OAuth token, which then expires after an hour. The data isn't stored anywhere.
#### Do I have to pay anything?
No, the software is free and will remain that way.
#### Will this get me banned on RPAN/Reddit?
No! Many people have been streaming using this method, nobody gets in trouble for it.
#### Are you planning to release it on Mac OS/Linux?
Yes, it's on my to-do list.

## Downloads
Go to [releases](https://github.com/warpspeedchic/retriever_for_rpan/releases/) for downloads.

If you need free streaming software, I recommend [OBS](https://obsproject.com/download).

## How to use
#### You will need:
- Retriever for RPAN
- any streaming software with RTMP support (the example below uses OBS Studio)

#### Setting up OBS to work with RPAN
1. Open OBS Studio
2. Go to File > Settings
3. Go to the Video tab
4. Set your Base Resolution to 1080x1920
5. Set your Output Resolution to 720x1280
6. Go to the Stream tab and for Service select 'Custom...'
7. Don't close this window yet!

#### Setting up the stream with Retriever
1. Open up the app
2. Click 'Authorize'
3. You will be redirected to Reddit, asking you to authorize 'reddit on Android' - click 'Allow'
4. You should see a 'Token obtained' page in the browser - you can then go back to Retriever
5. A couple of fields will show up. Enter the stream title, choose a subreddit and hit 'Set up the stream'
6. If the stream setup is successful, you will see your key and a server address
7. Copy the key and the server address to their corresponding fields in OBS
8. Click OK to apply the settings

And you're done. You can now press 'Start streaming' in OBS and close Retriever.