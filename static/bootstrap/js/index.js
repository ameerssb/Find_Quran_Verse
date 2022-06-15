//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

//Model 
//none

//View
var microphoneButton = document.getElementsByClassName("start-recording-button")[0];
var recordingControlButtonsContainer = document.getElementsByClassName("recording-contorl-buttons-container")[0];
var stopRecordingButton = document.getElementsByClassName("stop-recording-button")[0];
var cancelRecordingButton = document.getElementsByClassName("cancel-recording-button")[0];
var elapsedTimeTag = document.getElementsByClassName("elapsed-time")[0];
var microphoneButton = document.getElementsByClassName("start-recording-button")[0];
var spinner = document.getElementsByClassName("spinner-border")[0];
var arabicAlphabetDigits = /[\u0600-\u06FF]/;
var AlphabetDigits = /[a-zA-Z0-9]/;
//var closeBrowserNotSupportedBoxButton = document.getElementsByClassName("close-browser-not-supported-box")[0];
//var overlay = document.getElementsByClassName("overlay")[0];
//var audioElement = document.getElementsByClassName("audio-element")[0];
//var audioElementSource = document.getElementsByClassName("audio-element")[0]
//    .getElementsByTagName("source")[0];
//var textIndicatorOfAudiPlaying = document.getElementsByClassName("text-indication-of-audio-playing")[0];

//Listeners

//Listen to start recording button
microphoneButton.onclick = startAudioRecording;

//Listen to stop recording button
stopRecordingButton.onclick = stopAudioRecording;

//Listen to cancel recording button
cancelRecordingButton.onclick = cancelAudioRecording;

//Listen to when the ok button is clicked in the browser not supporting audio recording box
//closeBrowserNotSupportedBoxButton.onclick = hideBrowserNotSupportedOverlay;

//Listen to when the audio being played ends
//audioElement.onended = hideTextIndicatorOfAudioPlaying;

/** Displays recording control buttons */
function handleDisplayingRecordingControlButtons() {
    //Hide the microphone button that starts audio recording
    microphoneButton.style.display = "none";

    //Display the recording control buttons
    recordingControlButtonsContainer.classList.remove("hide");

    //Handle the displaying of the elapsed recording time
    handleElapsedRecordingTime();
}

/** Hide the displayed recording control buttons */
function handleHidingRecordingControlButtons() {
    //Display the microphone button that starts audio recording
    microphoneButton.style.display = "block";

    //Hide the recording control buttons
    recordingControlButtonsContainer.classList.add("hide");

    //stop interval that handles both time elapsed and the red dot
    clearInterval(elapsedTimeTimer);
}

/** Displays browser not supported info box for the user*/
function displayBrowserNotSupportedOverlay() {
    overlay.classList.remove("hide");
}

/** Displays browser not supported info box for the user*/
function hideBrowserNotSupportedOverlay() {
    overlay.classList.add("hide");
}

/** Creates a source element for the the audio element in the HTML document*/
function createSourceForAudioElement() {
    let sourceElement = document.createElement("source");
    audioElement.appendChild(sourceElement);

    audioElementSource = sourceElement;
}

/** Display the text indicator of the audio being playing in the background */
function displayTextIndicatorOfAudioPlaying() {
    textIndicatorOfAudiPlaying.classList.remove("hide");
}

/** Hide the text indicator of the audio being playing in the background */
function hideTextIndicatorOfAudioPlaying() {
    textIndicatorOfAudiPlaying.classList.add("hide");
}

//Controller

/** Stores the actual start time when an audio recording begins to take place to ensure elapsed time start time is accurate*/
var audioRecordStartTime;

/** Stores the maximum recording time in hours to stop recording once maximum recording hour has been reached */
var maximumRecordingTimeInHours = 0.00833333;

/** Stores the reference of the setInterval function that controls the timer in audio recording*/
var elapsedTimeTimer;

/** Starts the audio recording*/
function startAudioRecording() {

	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    
    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();


		/*  assign to gumStream for later use  */
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

        //store the recording start time to display the elapsed time according to it
        audioRecordStartTime = new Date();

        //display control buttons to offer the functionality of stop and cancel
        handleDisplayingRecordingControlButtons();
        
		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
          handleHidingRecordingControlButtons();
	});

}

/** Cancel the currently started audio recording */
function cancelAudioRecording() {
    console.log("Canceling audio...");

    //cancel the recording using the audio recording API
    rec.clear();

    //stop microphone access
	gumStream.getAudioTracks()[0].stop();

    //hide recording control button & return record icon
    handleHidingRecordingControlButtons();
}

/** Stop the currently started audio recording & sends it
 */
function stopAudioRecording() {

    console.log("stopButton clicked");
	
	//tell the recorder to stop the recording
	rec.stop();

    handleHidingRecordingControlButtons();

	microphoneButton.classList.add("visually-hidden");

	spinner.classList.remove("visually-hidden");

    //stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
    console.log("Stopping Audio Recording...");

}


function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);

	//name of .wav file to use during upload and download (without extendion)
	var filename = new Date().toISOString();

	filename = filename + ".wav";
	search(blob, filename);
}

function search(blob, filename){
	var form=new FormData();
		  form.append("file",blob, filename);
		  $.ajax({
			url: "/hello",
			method: "POST",
			processData: false,
			mimeType: "multipart/form-data",
			contentType: false,
			data: form,
			  	async: true,
			  	cache: false,
			  	timeout: 30000           
		  })
		  .done(function(data){
			const x = JSON.parse(data)
			let test = '';
			for (var i = 0; i<Object.keys(x.sura).length; i++){
				test += `Sura Chapter: ${x.sura[i]} \nSura Name: ${x.Sura_Name[i]} \nVerse Number: ${x.aya[i]} \nArabic Text: ${x.text[i]} \n\n`;
			}
			window.alert(test);	
			})
			.fail(function(jqXHR, textStatus){
				window.alert("Server "+textStatus);
			})
			.always(function(jqXHR, textStatus){
				microphoneButton.classList.remove("visually-hidden");

				spinner.classList.add("visually-hidden");
			})
}

function searchfind (){
	var invalidText = document.getElementById("invalidfile")
	var invalid = document.getElementById("file");
	if (!(invalidText.classList.contains("visually-hidden"))){
		invalidText.classList.add("visually-hidden");
	}
	if(invalid.value.length == 0){
		invalidText.classList.remove("visually-hidden");
	}
	else if(invalidText.classList.contains("visually-hidden")) {
		var button = document.getElementById("audiobutton");
		var textspin = document.getElementById("filespin")
		button.disabled = true; 
	//	button.innerText = "Loading..."; 
		textspin.classList.remove("visually-hidden");
		var form = new FormData();
		var files = document.getElementById("file").files;
		var file = files[0];
		form.append("file", file, file.name);
					$.ajax({
					url: "/hello",
					method: "POST",
					processData: false,
					mimeType: "multipart/form-data",
					contentType: false,
					data: form,
					async: true,
					cache: false,
					timeout: 30000
				})
				.done(function(data){
						const x = JSON.parse(data)
						let test = '';
						for (var i = 0; i<Object.keys(x.sura).length; i++){
							test += `Sura Chapter: ${x.sura[i]} \nSura Name: ${x.Sura_Name[i]} \nVerse Number: ${x.aya[i]} \nArabic Text: ${x.text[i]} \n\n`;
						}
						window.alert(test);	
				})
				.fail(function(jqXHR, textStatus){
					window.alert("Server "+textStatus);
				})
				.always(function(jqXHR, textStatus){
					textspin.classList.add("visually-hidden");
					//button.innerText = "Find Verse"; 
					button.disabled = false;								

			})
		}	
    }

$("#Text").on("keypress", function (event) {
	var invalidText = document.getElementById("invalidtext");
	var invalid = document.getElementById("Text");
	var key = String.fromCharCode(event.which);

   if (arabicAlphabetDigits.test(key) && arabicAlphabetDigits.test(invalid.value)) {
		if (!(invalidText.classList.contains("visually-hidden"))){
			invalidText.classList.add("visually-hidden");
		}
	}
	else if (arabicAlphabetDigits.test(key)) {
		if (!(invalidText.classList.contains("visually-hidden"))){
			invalidText.classList.add("visually-hidden");
		}
	}
	else if(AlphabetDigits.test(invalid.value) == true){
		invalidText.classList.remove("visually-hidden");
	}
	else if(key==' '){
		if (!(invalidText.classList.contains("visually-hidden"))){
			invalidText.classList.add("visually-hidden");
		}
	}
	else{
		invalidText.classList.remove("visually-hidden");
	}
   });

   $('#arabicCheck').on("paste", function (event) {
	var invalidText = document.getElementById("invalidtext");
	var invalid = document.getElementById("Text");
	var key = String.fromCharCode(event.which);
		if (arabicAlphabetDigits.test(invalid.value)) {
			if (!(invalidText.classList.contains("visually-hidden"))){
				invalidText.classList.add("visually-hidden");
			}
		}else{
			invalidText.classList.remove("visually-hidden");
		}

	});

function searchfindText (){
		var invalid = document.getElementById("Text");
		var invalidText = document.getElementById("invalidtext");
		if (!(invalidText.classList.contains("visually-hidden"))){
			invalidText.classList.add("visually-hidden");
		}	
		if(invalid.value.length == 0 || AlphabetDigits.test(invalid.value) == true){
			invalidText.classList.remove("visually-hidden");
		}
		else if(invalidText.classList.contains("visually-hidden")) {
			var button = document.getElementById("textbutton");
			var textspin = document.getElementById("textspin")	
			button.disabled = true;
	//		button.innerText = "Loading..."; 
			textspin.classList.remove("visually-hidden");
			var form = new FormData();
			form.append("arabic", $('#Text').val());
						$.ajax({
						url: "/translator",
						method: "POST",
						processData: false,
						mimeType: "multipart/form-data",
						contentType: false,
						data: form,
						async: true,
						cache: false,
						timeout: 30000           
					})
					.done(function(data){
						const x = JSON.parse(data)
						let test = '';
						for (var i = 0; i<Object.keys(x.sura).length; i++){
							test += `Sura Chapter: ${x.sura[i]} \nSura Name: ${x.Sura_Name[i]} \nVerse Number: ${x.aya[i]} \nArabic Text: ${x.text[i]} \n\n`;
						}
						window.alert(test);	
					})
					.fail(function(jqXHR, textStatus){
						window.alert("Server "+textStatus);
					})	
					.always(function(jqXHR, textStatus){
						textspin.classList.add("visually-hidden");
						//button.innerText = "Find Verse"; 
						button.disabled = false;								
					})			
		}
	}


/** Computes the elapsed recording time since the moment the function is called in the format h:m:s*/
function handleElapsedRecordingTime() {
    //display inital time when recording begins
    displayElapsedTimeDuringAudioRecording("00:00");

    //create an interval that compute & displays elapsed time, as well as, animate red dot - every second
    elapsedTimeTimer = setInterval(() => {
        //compute the elapsed time every second
        let elapsedTime = computeElapsedTime(audioRecordStartTime); //pass the actual record start time
        //display the elapsed time
        displayElapsedTimeDuringAudioRecording(elapsedTime);
    }, 1000); //every second
}

/** Display elapsed time during audio recording
 * @param {String} elapsedTime - elapsed time in the format mm:ss or hh:mm:ss 
 */
function displayElapsedTimeDuringAudioRecording(elapsedTime) {
    //1. display the passed elapsed time as the elapsed time in the elapsedTime HTML element
    elapsedTimeTag.innerHTML = elapsedTime;

    //2. Stop the recording when the max number of hours is reached
    if (elapsedTimeReachedMaximumNumberOfHours(elapsedTime)) {
        stopAudioRecording();
    }
}

/**
 * @param {String} elapsedTime - elapsed time in the format mm:ss or hh:mm:ss  
 * @returns {Boolean} whether the elapsed time reached the maximum number of hours or not
 */
function elapsedTimeReachedMaximumNumberOfHours(elapsedTime) {
    //Split the elapsed time by the symbo :
    let elapsedTimeSplitted = elapsedTime.split(":");

    //Turn the maximum recording time in hours to a string and pad it with zero if less than 10
    let maximumRecordingTimeInHoursAsString = maximumRecordingTimeInHours < 10 ? "0" + maximumRecordingTimeInHours : maximumRecordingTimeInHours.toString();

    //if it the elapsed time reach hours and also reach the maximum recording time in hours return true
    if (elapsedTimeSplitted.length === 3 && elapsedTimeSplitted[0] === maximumRecordingTimeInHoursAsString)
        return true;
    else //otherwise, return false
        return false;
}

/** Computes the elapsedTime since the moment the function is called in the format mm:ss or hh:mm:ss
 * @param {String} startTime - start time to compute the elapsed time since
 * @returns {String} elapsed time in mm:ss format or hh:mm:ss format, if elapsed hours are 0.
 */
function computeElapsedTime(startTime) {
    //record end time
    let endTime = new Date();

    //time difference in ms
    let timeDiff = endTime - startTime;

    //convert time difference from ms to seconds
    timeDiff = timeDiff / 1000;

    //extract integer seconds that dont form a minute using %
    let seconds = Math.floor(timeDiff % 60); //ignoring uncomplete seconds (floor)

    //pad seconds with a zero if neccessary
    seconds = seconds < 10 ? "0" + seconds : seconds;

    //convert time difference from seconds to minutes using %
    timeDiff = Math.floor(timeDiff / 60);

    //extract integer minutes that don't form an hour using %
    let minutes = timeDiff % 60; //no need to floor possible incomplete minutes, becase they've been handled as seconds
    minutes = minutes < 10 ? "0" + minutes : minutes;

    //convert time difference from minutes to hours
    timeDiff = Math.floor(timeDiff / 60);

    //extract integer hours that don't form a day using %
    let hours = timeDiff % 24; //no need to floor possible incomplete hours, becase they've been handled as seconds

    //convert time difference from hours to days
    timeDiff = Math.floor(timeDiff / 24);

    // the rest of timeDiff is number of days
    let days = timeDiff; //add days to hours

    let totalHours = hours + (days * 24);
    totalHours = totalHours < 10 ? "0" + totalHours : totalHours;

    if (totalHours === "00") {
        return minutes + ":" + seconds;
    } else {
        return totalHours + ":" + minutes + ":" + seconds;
    }
}