$(document).ready(function() {
	$('.comments .error').hide();
	$('.reply-btn').click(function(){
		var get_comment_id = $(this).parent('.col-sm-2').parent('.row').find('.reply').attr('id');
		var get_reply_content = $(this).parent('.col-sm-2').parent('.row').find('.reply').val();
		if (get_reply_content == '') {
			$(this).parent('.col-sm-2').parent('.row').find('.reply').addClass('is-invalid');
			$(this).parent('.col-sm-2').parent('.row').find('.error').show();
		} else {
			$.ajax({
				contentType: 'application/json',
				data:  JSON.stringify({ "comment_id": get_comment_id , "content":get_reply_content }),
				dataType: 'json',
				type: 'POST',
				url: '/create-new-reply/',
				headers: { "X-CSRFToken": $.cookie("csrftoken") },
				success: function(data){
					window.location.reload();
				},
				error: function(){
					console.log("Device control failed");
				},
			});
		}
	})
});