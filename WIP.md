### Twitch Work:
- [ ] Create python app that can process [RTMP](https://www.wowza.com/blog/rtmp-streaming-real-time-messaging-protocol) messages (streaming server). #task1
- [ ] Create basic authentication. #task2
- [ ] Create simple data structure to keep a time-series data set of the quality of the input stream and do some data processing offline.
- [ ] Add re-stream capability -- forward input to stream provider using ffmpeg. #task3
- [ ] Add support for simultaneous streaming. #task4
- [ ] Setup OBS -- document the process -- to stream to the service. #task5
- [ ] Deploy service to cloud infraestructure. (ligthweight CPU instance is enough, shouldn't need to perform any transcoding). #task6
- [ ] Create CI/CD pipelines to auto build and deploy latest commit to prod branch? #task7
- [ ] Configure repo rules for PR approvals and merge requirements. Also create templates for the issues section to add them to the work board. Outline PR process on wiki #task8

### Subtasks

#task1:
- [x] Install latest python, pip, and conda
- [x] Create barebones git repo and save dependency requirements.
- [x] Publish github repo with code.
- [x] Save conda `venv` to vcs if possible
- [ ] Expose endpoint to consume RMTP or RIST

#task2 :
- [ ] Implement simple JWT login in python (look for lib to do it with flask or django)
- [ ] Save authentication and account data to mongo collection

#task3 #task4 :
- [ ] Abstract implementation that handles the optimal setting configs for each live-stream server target.
- [ ] Write function that automatically transcodes input stream -- h.264 for now, but more codecs later -- to the optimal stream settings for the given target.
- [ ] Test functionality live and stream to two sources.

 #task5:
 - [ ] Create a README briefly going over what the setup process is.
 - [ ] Create a WIKI on github going into more detail.
 - [ ] Track work using github kanban/projects
 - [ ] Create quick install scripts.