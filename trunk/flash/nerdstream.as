﻿package {		import br.com.stimuli.loading.BulkLoader;    import br.com.stimuli.loading.BulkProgressEvent;	import br.com.stimuli.loading.BulkErrorEvent;		import gs.TweenLite;		import fl.containers.ScrollPane;	import fl.controls.ProgressBar;	import fl.events.ScrollEvent;	import flash.events.MouseEvent;	import flash.geom.Point;	import flash.filters.DropShadowFilter; 	import flash.display.*;	import flash.net.URLRequest;	import flash.events.*;	import flash.text.*;	import fl.motion.easing.*;	public class nerdstream extends Sprite {		// class constants		private var _DOMAIN:String = "http://yankee.sierrabravo.net/";				// image size data		private var _SHOTWIDTH:Number = 220;		private var _SHOTHEIGHT:Number = 165;		private var _NAMEBOXWIDTH:Number = 165;		private var _CELLSPACING:Number = 2;		private var _HEADERHEIGHT:Number = 101;		private var _TIMETABLEHEIGHT:Number = 25;				private var _loader:BulkLoader = new BulkLoader("nerdStreamImages");		private var _sp:ScrollPane;		private var _imageArea:MovieClip = new MovieClip();				private var _username:String;				private var _starttime:Number = 1000;		private var _endtime:Number = 1700;		private var _captureinterval:Number = 5;		private var _year:String = "2008";		private var _month:String = "07";		private var _day:String = "03";				private var _ndi:noDataImage = new noDataImage(0, 0);				public function get scrollPane():ScrollPane {			return _sp;		}				public function loadNerd(username:String, gridPositionY:Number, empName:String, empTitle:String, color:uint) {			// load images from http://yankee.sierrabravo.net/~username/nerdstream/			var loadURL:String = this._DOMAIN + "~" + username + "/nerdstream/";						//this._loader.logLevel = BulkLoader.LOG_INFO;						var i:int;			var filename:String;			var gridPositionX:Number = 0;			var currentImageId:String;						// add the name block			drawNameBlock(empName, empTitle, color, gridPositionY);						// queue up the images			for (i = this._starttime; i <= this._endtime; i += this._captureinterval) {					// we need to pad the timestamp to conform to naming conventions					currentImageId = username + i + ":" + gridPositionX + ":" + gridPositionY;										// TODO:  There must be a better way to do this... wrapping time to next hour after it hits 59 minutes...					// switch this over to the date class eventually...										if (i == 960) i = 1000;					if (i == 1060) i = 1100;					if (i == 1160) i = 1200;					if (i == 1260) i = 1300;					if (i == 1360) i = 1400;					if (i == 1460) i = 1500;					if (i == 1560) i = 1600;					if (i == 1660) i = 1700;										if (i < 1000) { 						this._loader.add(loadURL + this._year + this._month + this._day + "T0" + i + ".jpg", {id:currentImageId, maxTries:1});					}					else {						this._loader.add(loadURL + this._year + this._month + this._day + "T" + i + ".jpg", {id:currentImageId, maxTries:1});					}										_loader.get(currentImageId).addEventListener(Event.COMPLETE, onImageLoaded);					_loader.get(currentImageId).addEventListener(BulkLoader.ERROR, onError);										gridPositionX++;			}		}				public function startDownloading():void {			// dispatched when ALL the items have been loaded:            this._loader.addEventListener(BulkLoader.COMPLETE, onAllItemsLoaded);			this._loader.addEventListener(BulkLoader.PROGRESS, onProgress);						// now start the loading            this._loader.start();		}				public function nerdstream():void {						// Create the scroll pane object, this is where we will draw all of our images onto			_sp = new ScrollPane();						_sp.move(0, _HEADERHEIGHT);			_sp.setSize(1200,623);			_sp.scrollDrag = true;			_sp.source = _imageArea;						addChild(_sp);			drawTimeTable();		}				private function drawTimeTable():void {			trace('drawing timetable');						var timeTable:Sprite = new Sprite();			timeTable.graphics.beginFill(0x000000);			timeTable.graphics.drawRect(0, 0, _SHOTWIDTH * 50, _TIMETABLEHEIGHT);			timeTable.graphics.endFill();						// set the formatting style			var fTime:TextFormat = new TextFormat();            fTime.font = "Georgia";            fTime.color = 0xFFFFFF;            fTime.size = 14;			fTime.align = "right";						var counter:Number = 0;			var i:Number = 0;									// loop through and display the time increments			for (i = this._starttime; i <= this._endtime; i += this._captureinterval) {				var lblTime:TextField = new TextField();								lblTime.width = _SHOTWIDTH;				lblTime.y = 2;				lblTime.x = (counter * _SHOTWIDTH) + (_CELLSPACING * counter);				lblTime.defaultTextFormat = fTime;				lblTime.text = i + 'am';								timeTable.addChild(lblTime);				counter++;			}						_imageArea.addChild(timeTable);		}				private function drawNameBlock(empName:String, empTitle:String, color:uint, row:Number) {			// this function simply draws a colored block on the appropriate row and fills it with			// the employee name and employee title						var nameBox:Sprite = new Sprite();			nameBox.graphics.beginFill(color);			nameBox.graphics.drawRect(0, (row * _SHOTHEIGHT + (_CELLSPACING * row)) + (_TIMETABLEHEIGHT + _CELLSPACING), _SHOTHEIGHT - 2, _SHOTHEIGHT);			nameBox.graphics.endFill();						// add a little inner-drop shadow			// nameBox.filters = [new DropShadowFilter(7, 315, 0x000000, .65, 6, 6, .5, 1, true, false, false)];						// set the formatting style			var formatName:TextFormat = new TextFormat();            formatName.font = "Verdana";            formatName.color = 0xFFFFFF;            formatName.size = 14;			formatName.align = "right";						// set the formatting style			var formatTitle:TextFormat = new TextFormat();            formatTitle.font = "Verdana";            formatTitle.color = 0xFFFFFF;            formatTitle.size = 12;			formatTitle.align = "right";						//Add the text labels			var labelName:TextField = new TextField();			var labelTitle:TextField = new TextField();						labelName.width = _SHOTHEIGHT - 10;			labelName.x = 5;			labelName.y = (row * _SHOTHEIGHT + (_TIMETABLEHEIGHT + _CELLSPACING)) + (_CELLSPACING * row) + 5;			labelName.defaultTextFormat = formatName;			labelName.text = empName;						labelTitle.width = _SHOTHEIGHT - 10;			labelTitle.x = 5;			labelTitle.y = (row * _SHOTHEIGHT + (_TIMETABLEHEIGHT + _CELLSPACING)) + (_CELLSPACING * row) + 24;			labelTitle.defaultTextFormat = formatTitle;			labelTitle.wordWrap = true;			labelTitle.text = empTitle;						nameBox.addChild(labelTitle);			nameBox.addChild(labelName);						_imageArea.addChild(nameBox);		}				private function onAllItemsLoaded(evt:Event):void {			trace('everything done loading.');						_sp.refreshPane();		}				private function onImageLoaded(e:Event):void {			addImageToScrollPane(e.target.id);		}				function onProgress(e:BulkProgressEvent):void{		   //trace(e.percentLoaded);		}				private function addImageToScrollPane(id:String):void {						var shotData:Array = id.split(":");						var b:Bitmap = _loader.getBitmap(id);			b.alpha = 1;			b.x = shotData[1] * _SHOTWIDTH + _NAMEBOXWIDTH + (_CELLSPACING * shotData[1]);			b.y = shotData[2] * _SHOTHEIGHT + (_TIMETABLEHEIGHT + _CELLSPACING) + (_CELLSPACING * shotData[2]);			b.width = _SHOTWIDTH;			b.height = _SHOTHEIGHT;						// this will make the images fade in nicely			_imageArea.addChild(b);						TweenLite.from(b, 1.2, {alpha:0, ease:Linear.easeIn});						_sp.refreshPane();		}		private function onError(e:BulkErrorEvent ) : void{			// determine grid position from id (id:col:row);			var shotData:Array = e.target.id.split(":");						// load the no-picture image if there is no picture for this timeframe			var b:Bitmap = new Bitmap(_ndi);						b.x = shotData[1] * _SHOTWIDTH + _NAMEBOXWIDTH + (_CELLSPACING * shotData[1]);			b.y = shotData[2] * _SHOTHEIGHT + (_TIMETABLEHEIGHT + _CELLSPACING) + (_CELLSPACING * shotData[2]);			b.width = _SHOTWIDTH;			b.height = _SHOTHEIGHT;						this._imageArea.addChild(b);			_sp.refreshPane();		}				public function onAllItemsProgress(evt:Event):void {					}					}	}