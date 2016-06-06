$(function() {
	$('#form_categoria').change(function() {
		var subcat = $('#form_subcategoria')
		var cat_val = $('#form_categoria').val()
		subcat.empty()
		var childs = "<option>-</option>"
		if ( cat_val == 'Apartahoteles') {
			for ( var i = 1 ; i < 6 ; i++) {
				childs += "<option>"+ i +" llaves</option>\n"
			}
		}else if (  cat_val == 'Residencias universitarias'  || cat_val == 'Albergues'  )  {
			;
		}else {
			childs += "<option>1 estrella</option>\n"
			for ( var i = 2 ; i < 6 ; i++) {
				childs += "<option>"+ i +" estrellas</option>\n"
			}
			childs += "<option>5 estrellas Gran Lujo</option>\n"
		}
		subcat.append(childs)
	})
})