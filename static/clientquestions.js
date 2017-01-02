
function init () {
    numoflevels = levels.length;
    initialised = true;
    var arr1 = [];
    var arr2 = [];
    if (currentlevel>=numoflevels) {currentlevel = numoflevels-1}
  
    arr1 = levels[currentlevel]["qarray"];
    arr2 = levels[currentlevel]["aarray"];
    currentQInstructions = levels[currentlevel]["instructions"];
    numNeeded = levels[currentlevel]["numNeeded"];
    currentNeeded = numNeeded;
    resetOnMistake = levels[currentlevel]["resetOnMistake"];
    clearAnswer = levels[currentlevel]["clearAnswer"];
    
    currentRandomArray = createRandomArray(arr1,arr2);
}







// var level0qarray = [
//     "good","bad","far","big","tall","interesting","beautiful","friendly","pretty","large","fast","clean","dirty","crazy","confusing"];


// var level0answers = [
//     "better","worse","farther/further","bigger","taller","more interesting","more beautiful","friendlier/more friendly","prettier/more pretty","larger","faster","cleaner","dirtier","crazier","more confusing"];

// var level1qarray = [
//     "good","bad","far","big","tall","interesting","beautiful","friendly","pretty","large","fast","clean","dirty","crazy","confusing"];

// var level1answers = ["the best","the worst","the farthest/the furthest","the biggest","the tallest","the most interesting","the most beautiful","the friendliest/the most friendly","the prettiest/the most pretty","the largest","the fastest","the cleanest","the dirtiest","the craziest","the most confusing"];


// var level2qarray = [
//     "My brother's room is _______________ (tidy) mine.","Australia is _________________ (big) England.","I feel _______________ (good) yesterday.","He thinks Chinese is ______________(difficult) language in the world","Valencia played _________________(bad) Real Madrid yesterday.","Cats are not ____________________ (intelligent) as dogs.","Show me ____________________ (good) restaurant downtown.","________________ (hot) desert of all is the Sahara and it's in Africa.","Who is ________________(talkative) person in your family?"
// ];


// var level2answers = [
//     "tidier than","bigger than","better than","the most difficult","worse than","as intelligent","the best","The hottest/the hottest","the most talkative"];


// var level3qarray =
//     ["elephant / mouse / bigger / is / than / An / a / .","in / world / the / river / Amazon / The / is / longest / river / the / .","older / father / mother / my / My / is / than / .","today / Lady / craziest / celebrity / Gaga / the / is /.","plane / a / car / Is / faster / a / than / ?"];

// var level3answers =     
//     ["An elephant is bigger than a mouse.","The Amazon is the longest river in the world.","My father is older than my mother./My mother is older than my father.","Lady Gaga is the craziest celebrity today.","Is a plane faster than a car?/Is a car faster than a plane?"];




// pres simp

var level0qarray = ["I __________ (eat) Pizza. ","We all __________ (study) English. ","You _________(not go) to Muscat.","My sister and I _________ (not want) to see that movie. ","_____________ (you like) jazz music? ","Where _____________ (he go) shopping?","Who __________ (be) ready for a break?","The girls _________ (not enjoy) football. ","The boys __________ (not know) how to cook well. ","My brother _________ (not speak) French. "];


var level0answers = ["eat","study","don't go/do not go","do not want/don't want","Do you like","does he go","is","don't enjoy/do not enjoy","don't know/do not know","doesn't speak/does not speak"];



// write the ing

var level1qarray = ["come","sit","travel","stop","run","have","get","think","sell","go","do","buy"];


var level1answers = ["coming","sitting","travelling","stopping","running","having","getting","thinking","selling","going","doing","buying"];


//present cont
var level2qarray = ["I __________ (eat) Pizza. ","We __________ (study) English. ","You _________(not go) to Muscat.","Where _____________ (he go) shopping?","The girls _________ (not enjoy) the football game. ","My brother _________ (not speak) French. ","What ____________(you do) for your project?","Why __________ (she not come) to class. ","Those students ____________(not carry) books.","She ______________(drive) a Bentley."];



var level2answers = ["am eating","are studying","are not going/aren't going","is he going","are not enjoying/aren't enjoying","isn't speaking/is not speaking","are you doing","isn't she coming/is she not coming","are not carrying/aren't carrying","is driving"];




// write the past tense 

var level3qarray = ["be","have","go","do","eat","bring","drive","make","become","fly","give","ride","sell","think","understand","buy"];

    
var level3answers = ["was/were","had","went","did","ate","brought","drove","made","became","flew","gave","rode","sold","thought","understood","bought"];    

  

// past smip

var level4qarray = ["I __________ (eat) Pizza. ","We all __________ (study) English. ","You _________(not go) to Muscat.","My sister and I _________ (not want) to see that movie. ","_____________ (you like) jazz music? ","Where _____________ (he go) shopping?","Who __________ (be) ready for a break?","The girls _________ (not enjoy) football. ","The boys __________ (not know) how to cook well. ","My brother _________ (not speak) French. "];

var level4answers = ["ate","studied","didn't go/did not go","didn't want/did not want","Do you like","did he go","was","did not enjoy/didn't enjoy","did not know/didn't know","did not speak/didn't speak"];



// mixed words (adverbs of freq)

var level5qarray= [ "/ movies / go / They / often / to / the / .","/ never / Sara / smiles / .","/sometimes / reads / He / newspaper / the / .","/ mornings / usually / go / I / running / the / in /.","/ evenings / watch / television / always / the / We / in /.","/ She / homework / helps / daughter / never / her / her / with /."];

var level5answers = ["They often go to the movies.","Sara never smiles.","He sometimes reads the newspaper.","I usually go running in the mornings.","We always watch television in the evenings.","She never helps her daughter with her homework."];









//mixed tenses

var level6qarray =  ["This _______ (be) Mark.","He _______ (wear) a t-shirt and shorts today.","Mark _______ (like) fruits and vegetables. ","Sue _______ (eat) a banana at the moment. ","Sue ________ (eat) some fruit everyday. ","Look, Jenny and Jill ________ (go) to school. ","Jenny and Jill usually _______ (cycle) to school. ","The weather is good today. It __________ (not rain).","What ___________(they do) tomorrow?","What ___________ (they do) on Tuesdays?","What ___________(they do) yesterday?","We _______(have) a test last week.","She ______ (not go) to Muscat two days ago."];

var level6answers = ["is","is wearing","likes","is eating","eats","are going","cycle","isn't raining/is not raining","are they doing","do they do","did they do","had","did not go"];



//var level8qarray = ["I __________ (eat) Pizza. ","We __________ (study) English. ","You _________(not go) to Muscat.","Where _____________ (he go) shopping?","The girls _________ (not enjoy) the football game. ","My brother _________ (not speak) French. ","What ____________(you do) for your project?","Why __________ (she not go) to class. ","Those students ____________(not carry) books.","She ______________(drive) a Bentley."];

//var level8answers = ["was eating","were studying","were not going/weren't going","was he going","were not enjoying/weren't enjoying","wasn't speaking/was not speaking","were you doing","wasn't she going/was she not going","were not carrying/weren't carrying","was driving"];

//var level9qarray = ["I ___________ (run) in the park when two cats crossed my way. ","Robert ________ (fall) off the ladder when he was picking cherries.","When we ___________ (travel) around Ireland, we met some nice people. ","While she __________ (speak) on the phone, the kettle boiled. ","When I __________(leave) the house this morning, the sun was shining. ","She ________(laugh) when she heard the joke. ","They saw the bus and _______ (run) to catch it. ","They were very happy when they ________(receive) their midterm results. ","What ______________(do / you) yesterday at 8pm?","Why ____________ (ring / not / you) me yesterday?"];


//var level9answers = ["was running","fell","were travelling/travelled","was speaking","left","laughed","ran","received","were you doing","didn't you ring/did you not ring"];

//var level10qarray = ["/ parents / listen / radio / car / My / always / the / the / in / to / . ","/ home / wasn’t / because / went / Fatima / she / well / feeling / .","/ have / does / brothers / Ali / any / or / sisters / not / .","/ sister / hospital / Doesn’t / work / the / at / your / ?  ","/ French / speaks / and / Our / teacher / from / comes / Canada /.","/ was / I / you / a / called / When / meeting / having / , / ."];

//var level10answers = ["My parents always listen to the radio in the car.","Fatima went home because she wasn't feeling well.","Ali does not have any brothers or sisters./Ali does not have any sisters or brothers.","Doesn't your sister work at the hospital?","Our teacher speaks French and comes from Canada./Our teacher comes from Canada and speaks French.","When you called, I was having a meeting."];



var currentRandomArary;    
var currentquestion = 0;
var currentlevel = 0;
//var numoflevels = levels.length();
var numoflevels = 0;
var currentQInstructions;
var currentQString;
var currentAnswer;
var initialised = false;
var currentNeeded;
var numNeeded;
var finbool = "false";



function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
    }
    return "";
} 




function getCookies () {
    var cn = getCookie("currentn");
    var cl = getCookie("currentl");
    var fin = getCookie("finished");
    if (cl!="") {
	currentlevel = parseInt(cl);
	init();
    }
    if (cn!="") {
	currentNeeded = parseInt(cn);
    }
    
    if (fin!="") {
    	finbool = fin;
    }
}

function setCookies () {
    setCookie("currentn",currentNeeded,2);
    setCookie("currentl",currentlevel,2);
    setCookie("finished",finbool,2);
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
} 


function createRandomArray (qarray, answers) {
   var len = 0;
    var randomArray = [];
   if (qarray.length<=answers.length) {
	len = qarray.length;
   }
   else {
	len = answers.length;
   }
    
   for (i = 0; i<len; i++) {
	var tmpArray = [qarray[i],answers[i]];
	randomArray.push(tmpArray);

   }

   return new RandomArray(randomArray);
}





function checkAnswer(answer) {
    var answerarr = currentAnswer.split("/");
    var result = false;
    var trimmedanswer = $.trim(answer);
    for (i = 0; i<answerarr.length; i++) {
     	if (trimmedanswer.toLowerCase()==answerarr[i].toLowerCase()) {
     	    result = true;
     	}
     }
    return result;
}



function resetAll () {
currentlevel = 0;
    init();
    finbool="false";
    setCookies();
}


function nextQuestion () {
    tmp = currentRandomArray.splicearr();
    currentQString = tmp[0][0];
    currentAnswer = tmp[0][1];
    }




//////////////////////// randomarray object ///////////////////////////////////
///////    takes an array as a creation argument ////////////////
///////// object.splicearr sorts randomly through the array ////////////
////////// if object.true is true, it will loop, alternatively it will 
////////// stop looping after each member of the array has been given. 
////////// object.endmessage is the final message if loop is false. 


function RandomArray (thisarray) {
this.fullarray = thisarray;
this.temparray = thisarray.slice(0);
this.len = this.fullarray.length;
this.loop = true;
this.splicearr = function () {
this.len = this.fullarray.length;
if (this.len < 1 && this.loop == true) 
{
this.fullarray = this.temparray.slice(0);
this.len = this.fullarray.length;
}
if (this.len < 1) {
choice = this.endmessage;
} 
else {
node = Math.floor(Math.random()*this.len);
choice = this.fullarray.splice(node,1);
}
return choice;
	       
};
this.test = function () {
};
this.endmessage = "out of choices";
}


////////////////////////////////////////////////////////////////////////


