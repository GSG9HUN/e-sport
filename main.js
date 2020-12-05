

const Discord = require('discord.js');
const config = require('./config.json');
const ytdl = require('ytdl-core')
const client = new Discord.Client();

client.on('ready',()=>{

console.log('Bot is online');

});


client.login(config.token);
var client_on_voice = false;
var play_sender = null;
var joined_channel = null;

client.on('message',message =>{
    if(message.author.bot) 
    {
        return;
    }
    if(!message.content.startsWith(config.prefix) || message.author.bot){
        return ;
    }
    const args = message.content.slice(config.prefix.length).split(/ +/);
    const command = args.shift().toLowerCase();
    if(command==='hi'){
        message.channel.send('Hello '+message.author.username+'!');
    }else if(command ==='play' && (!client_on_voice || play_sender === message.author)){
       
      playert(message,args);
            
        
    }else if (command==='stop'){
        if(play_sender=== message.author){
           
            play_sender= null;
            joined_channel.leave()
            joined_channel=null;
            client_on_voice = false;
        }
    }else{
        message.channel.send("Invalid command");
    }

});




async function playert(message,args) {
   
    if(message.member.voice.channelID!== null && args[0])
    {
        if(args[0].startsWith("https://www.youtube.com/watch?")){
            var channelID = message.member.voice.channelID;
            
            var channel = client.channels.cache.get(channelID.toString());
            
            if(!channel) 
            {
                return console.error("The cahnnel does not exist");
            }

            const songinfo = await ytdl.getInfo(args[0]);
            const song = {
                title: songinfo.videoDetails.title,
                url: songinfo.videoDetails.video_url,
            };
            play_sender= message.author;
            joined_channel=channel;
            var connection = await channel.join(); 
            client_on_voice = true; 

            const dispatcher = connection;
            dispatcher.play(ytdl(song.url.toString(),{"volume": 0.5}));
            
            dispatcher.on('start',()=>{
                console.log("Audio started");
            })

            dispatcher.setVolume(0.25);
            

        }else{
            message.channel.send("Meg kell adnod egy youtube linket")
        }

    }
    else
    {
        if(message.member.voice.channelID=== null){
            message.channel.send("Be kell lépned egy voice channelbe")
        }else{
            message.channel.send("Meg kell adnond a linket")
        }
  }
}

