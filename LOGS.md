# 03/05 logs

Add work log here later.


# 03/04 Logs:
~ 14:00 -> 20:00 (6h total) work:
- [ ] Finish build battle plugin for danevent.
- [ ] Finish python grpc project and hook up model to rust backend.
- [ ] Create rust backend takes in REST calls and calls python grpc service to obtain predictions/outputs.

-
The following is for the work performed from 02:16 -> 05:00 on 03/04/2021, there might be some extra work after this, but I'll update this log as I go. The work below is for the open-restreamer-python project.

## Open Re-streamer (Python) #task1:
-
El setup initial del re-streamer repo took forever, so let's actually get the service working and deployed to a digital ocean instance, all tasks should take 2h TOPS. If not done, move on.
-
### Tasks / TO-DO(s):

- [ ] Fix build pipeline with linter. #p5
- [ ] Fix issue building container (i think we aren't copying all the repo files). #p3
- [ ] Figure out how to take in RMTP or RIST protocol on python app. #p1
- [ ] Use ffmpeg call from python to asyncrhonously re-stream the received feed to YT and TWITCH. #p2
- [ ] Add basic endpoints to start and stop transmission for user, put endpoint to update current stream title and other metadata on all platforms at once. #p5
- [ ] Implement JWT?? Just hardcode an auth token for now hahah. #p6
- [ ] Implement endpoint to sign up using github, twitch, twitter, or youtube. #p7
- [ ] Create front-end, stack should be: ***svelte + typescript + tailwindcss + redis + mongo + vercel + cloudflare-workers + docker&terraform + oAuth (AVOID) + stripe***. #p10

-

### 03/04 04:08 Update:

After some research on how to appropiately I have come to the realization that the architectture for this re-streamer tools is significantly simpler that I had originaly thought.

Basically, we need a multi-threaded application that does the following:
1. Thread 1 will always be waiting for REST calls and will server and return futures/signals.
2. Thread 2 will focus on taking in (as many as possible) RTMP/SRT/RIST feeds coming from an OBS emitter and will store the frames into something parseable for FFMPEG.
3. Thread 3 will looks at the changes on the buffer and automatically open multiple stream (multicast) connections to all the supported streaming platforms that the provided user has configured in their profile (for now, just youtube and twitch). We can use [PyLivestream](https://github.com/scivision/PyLivestream)  src code for this. Most of the heavy listing is already done by them, the code is a bit complex but we can take lots of inspiration from their approach.

Considering how tired I am, I will focus on implementing the less important part of this project, which is the authentification step. I'll be implementing a simple login with a basic mongodb query to check if auth token present in auth collection and verify that way. Super simple, but makes me introduce mongo to the project and adds some more endpoints that we'll inevitably have to write.

Given that, these are the tasks I shouls get done before leaving today:

- [ ] Deploy Mongo Atlas DB for open-restreamer-python.
- [ ] Connect Python project to mongo
- [ ] Add simple get endpoint that checks mongo collection for user and token provided in request being present in coll. If present, authentication is succesful, otherwise 403 forbidden.
- [ ] Add endpoints to create, view, and edit user profiles. This profiles will hold the user streaming keys, as well as other user preferences.
- [ ] Add type enforcement everywhere. Use dataclasses everywhere.
- [ ] Need to fix docker container file.