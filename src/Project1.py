# {{{Project File :Code }}} 
def Info() : 
    print(  " ::This is request to get info Plasse proviad the Follwong ::") 
    Name=input("Enter Your name") 
    VideosWathed= input(" Amount of videos you wathed")
    ScoreOFCoures=input("Your Scoer") 
    Monypaid=input("How much have you paid ?") 
    file=open("data/FileAnas.txt " ,"a")
    print(file.write( f" YourName:{Name} num of video you Witced:{VideosWathed} Score:{ScoreOFCoures} AmountofMonypaid:{Monypaid} \n") ) 
    
def WorkingOnfile (): 
    file = open("data/FileAnas.txt", "r", encoding="utf-8")
    lines = file.readlines()
    Totalsum = 0
    count = 0
    for line in lines:
        print(line.split())
    file.close()




Info()
WorkingOnfile()
         
