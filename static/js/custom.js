$(document).ready(function() {
	$.ajax({
		url: "/api/posts/",
		type: 'GET',
		dataType: 'json',
		success: function(res) {
			console.log(res);
		}
	})
});