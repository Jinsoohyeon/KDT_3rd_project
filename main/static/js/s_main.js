$(function() {

	$('select[multiple].active.3col').multiselect({
	  columns: 3,
	  placeholder: '선택',
	  search: true,
	  searchOptions: {
	      'default': '검색'
	  },
	  selectAll: true
	});

});
