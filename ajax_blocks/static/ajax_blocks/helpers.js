var render_ajax_blocks;
(function($) {
	var initial_request_done = false;
	function replace_blocks(data) {
		$.each(data, function(i, val) {
			var elem = $('*[data-block=' + i + ']:first');
			elem.html(val);
		});
	}
	render_ajax_blocks = function(url) {
		$.ajax(url, {
			success: function(data) {
				if (!initial_request_done) {
					if (typeof(history.replaceState) !== 'undefined') {
						var state = {};
						$.each(data.blocks, function(i, val) {
							state[i] = $('*[data-block=' + i + ']:first').html();
						});
						history.replaceState(state, null, window.location);
					}
					initial_request_done = true;
				}
				replace_blocks(data.blocks)
				if (typeof(history.pushState) !== 'undefined') {
					history.pushState(data.blocks, null, data.url)
				}
			}
		});
	}
	window.onpopstate = function(event) {
		replace_blocks(event.state);
	}
})(jQuery);
