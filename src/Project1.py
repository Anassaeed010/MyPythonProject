# {{{Project File :Code }}} 
def Info() : 
    print(  " ::This is request to get info Plasse proviad the Follwong ::") 
    Name=input("Enter Your name") 
    VideosWathed= input(" Amount of videos you wathed")
    ScoreOFCoures=input("Your Scoer") 
    Monypaid=input("How much have you paid ?") 
    file=open("data/FileAnas.txt " ,"a")
    print(file.write( f" YourName:{Name} num of video you Witced:{VideosWathed} Score:{ScoreOFCoures} AmountofMonypaid:{Monypaid} \n") ) 
    

Info()    
         
