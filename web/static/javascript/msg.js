function get_url(url,json){
	url += "?"
	for(var key in json){
		url = url + key + "=" +json[key]+"&"
	}
	return url
}

function get_r(key_val,max_r){
	sum = 0
	r = new Array()
	for(var i in key_val){
		sum += key_val[i]['val']
	}
	for(var i in key_val){
		r[i] = Math.sqrt(key_val[i]['val']/sum)*max_r
	}
	return r
}

//var seed_s = 1
var seed_s = Number(new Date())
function get_random(min_num,max_num){
	seed_s = ( seed_s * 9301 + 49297 ) % 233280;
	var x = ( seed_s * 9301 + 49297 ) % 233280/233280.0 ;
	x = x*(max_num-min_num);
	x = x+min_num;
	x = Math.round(x);
	return x;
}

var width = window.innerWidth
var height = 640
var border = 5

function xy_valid(cur_xy,cur_r,xy,rs,n){
	if(n <=0) return true
	for(var i=n-1;i>=0;i--){
		var dis,rr;
		dis = Math.sqrt(Math.pow((cur_xy['x']-xy[i]['x']),2)+Math.pow((cur_xy['y']-xy[i]['y']),2))
		//rr = Math.max(cur_r,rs[i])
		rr = cur_r+rs[i]
		//console.log("dis:"+dis)
		//console.log("rr:"+rr)
		if(dis < rr) return false
	}
	return true
}

function get_xy(rs){
	xy = new Array()
	var n = 0
	for(var i=0;i<rs.length;i++){
		cur = new Array()
		do{
			cur['x'] = get_random(rs[i],width-rs[i])
			cur['y'] = get_random(rs[i],height-rs[i])
		}
		while(xy_valid(cur,rs[i],xy,rs,n)==false)
		xy[n] = cur
		n++
	}
	return xy
}

var color = new Array("220,20,60","255,105,180","255,0,0","255,165,0","255,222,173","210,105,30","255,255,0","255,215,0"," 	189,183,107","0,255,127","50,205,50","0,128,0","65,105,225","0,191,255","0,255,255","128,0,128","148,0,211"," 	123,104,238");

function draw(key_val, canvas_all){
	canvas_all.width = width; 
	canvas_all.height = height; 

	var canvas = canvas_all.getContext('2d');
	canvas.fillStyle='#f1f1f1';
	canvas.fillRect(0,0,width,height);
	
	rs = get_r(key_val,height/2.75)
	xy = get_xy(rs)
	//console.log(rs)
	//console.log(xy)	

	for(var i=0;i<rs.length;i++){
		if(rs[i] <= 0) continue
		canvas.beginPath();
		canvas.arc(xy[i]['x'],xy[i]['y'],rs[i],0,Math.PI*2,false);
		canvas.fillStyle = "rgba("+color[get_random(0,color.length-1)]+",0.8)";
		canvas.fill();
		canvas.closePath();
		if(rs[i] >= 10){
			draw_text(canvas,i+1,key_val[i],xy[i]['x'],xy[i]['y'])
		}
	}
}


function draw_text(canvas,ind,kv,x,y){
	fs = 13
	fps = fs/2
	canvas.font = "bold "+fs+"px Courier New";
    	canvas.fillStyle = "black";
	//txt1 = "["+ind +"]"+ kv['key']
	txt1 = kv['key']
	canvas.fillText(txt1,x-txt1.length/2*fps,y-fs/4);
	txt2 = "["+kv['val']+"]"
	canvas.fillText(txt2,x-txt2.length/2*fps,y+fs*3/4);
}
