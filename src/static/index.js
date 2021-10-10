function getAllBooks(k) {
	fetch("http://127.0.0.1:5000/getAllBooks")
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		})
		.then(data=> {
			const dataTmp = data;
			dataTmp.sort(compare);
			newArr = [];
			for (i = 0; i < k; i++) {
				newArr.push(dataTmp[i]);
			}
			console.log(newArr);
    		makeBookBarChart(newArr);
        });	
        
}

function compare( a, b ) {
  if (parseFloat(a.rating) < parseFloat(b.rating)) {
    return 1;
  }
  if (parseFloat(a.rating) > parseFloat(b.rating)){
    return -1;
  }
  return 0;
}

// used template from https://alignedleft.com/tutorials/d3/making-a-bar-chart
function makeBookBarChart(dataArr) {
	var w = 500;
	var h = 100;
	var barPadding = 15;
	if (d3.select("svg")) {
		d3.select("svg").remove(); 
	}
	var svg = d3.select("body")
				.append("svg")
				.attr("width", w)
				.attr("height", h);
	svg.selectAll("rect")
	   .data(dataArr)
	   .enter()
	   .append("rect")
	   .attr("x", function(d, i) {
	   		return i * (w / dataArr.length);
	   })
	   .attr("y", function(d) {
	   		return h - parseFloat(d.rating) * 15;
	   })
	   .attr("width", w / dataArr.length - barPadding)
	   .attr("height", function(d) {
	   		return parseFloat(d.rating) * 15;
	   })
	   .attr("fill", function(d) {
					return "rgb(0, 0, " + (parseFloat(d.rating) * 45) + ")";
		});
		
	svg.selectAll("text")
	   .data(dataArr)
	   .enter()
	   .append("text")
	   .text(function(d) {
	   		return 'Book : ' + d.book_id;
	   })
	   .attr("text-anchor", "middle")
	   .attr("x", function(d, i) {
	   		return i * (w / dataArr.length) + (w / dataArr.length - barPadding) / 2;
	   })
	   .attr("y", function(d) {
	   		return h - (parseFloat(d.rating) * 4) + 14;
	   })
	   .attr("font-family", "sans-serif")
	   .attr("font-size", "11px")
	   .attr("fill", "white");
	
}
function getAllAuthors(k) {
	fetch("http://127.0.0.1:5000/getAllAuthors")
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		})
		.then(data=> {
			const dataTmp = data;
			dataTmp.sort(compare);
			newArr = []
			for (i = 0; i < k; i++) {
				newArr[i] = dataTmp[i];
			} 
			console.log(newArr);
    		makeAuthorBarChart(newArr);
        });	       
}

// used template from https://alignedleft.com/tutorials/d3/making-a-bar-chart
function makeAuthorBarChart(dataArr) {
	var w = 500;
	var h = 100;
	var barPadding = 15;
	if (d3.select("svg")) {
		d3.select("svg").remove(); 
	}
	var svg = d3.select("body")
				.append("svg")
				.attr("width", w)
				.attr("height", h);
	svg.selectAll("rect")
	   .data(dataArr)
	   .enter()
	   .append("rect")
	   .attr("x", function(d, i) {
	   		return i * (w / dataArr.length);
	   })
	   .attr("y", function(d) {
	   		return h - parseFloat(d.rating) * 15;
	   })
	   .attr("width", w / dataArr.length - barPadding)
	   .attr("height", function(d) {
	   		return parseFloat(d.rating) * 15;
	   })
	   .attr("fill", function(d) {
					return "rgb(0, 0, " + (parseFloat(d.rating) * 45) + ")";
		});
		
	svg.selectAll("text")
	   .data(dataArr)
	   .enter()
	   .append("text")
	   .text(function(d) {
	   		return 'Author : ' + d.author_id;
	   })
	   .attr("text-anchor", "middle")
	   .attr("x", function(d, i) {
	   		return i * (w / dataArr.length) + (w / dataArr.length - barPadding) / 2;
	   })
	   .attr("y", function(d) {
	   		return h - (parseFloat(d.rating) * 4) + 14;
	   })
	   .attr("font-family", "sans-serif")
	   .attr("font-size", "11px")
	   .attr("fill", "white");
	
}

