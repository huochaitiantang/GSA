$(document).ready(function(){
	
	params = new Array()
	params['type'] = $('input[name=type][checked]').val()
	params['star_gap'] = $("select[name=star_gap] option[selected]").text()
	params['size_gap'] = $("select[name=size_gap] option[selected]").text()
	//console.log(params)
	url = get_url("/repos/statistics/msg",params)
	//console.log(url)
	request = new XMLHttpRequest()
	request.open('GET',url,true)
	request.addEventListener("load", show_res, false);
	request.send()	
		
	

	function show_res(evt){
		ans = JSON.parse(request.responseText);
		key_val = ans['key_val']
		console.log(ans)
		for(var i in key_val){
			key_val[i] = JSON.parse(JSON.stringify(key_val[i]))
			//console.log(key_val[i]["key"]+":"+key_val[i]["val"])
		}
		cas = document.createElement('canvas')
		draw(key_val, cas)
		document.body.appendChild(cas)

	}
	






})
