function handleGetBook(bookID) {
	var u = "http://127.0.0.1:5000/book?id=" +bookID
	console.log(u)
	fetch(u)
		.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
			console.log(data);
			const html = data.map(err => {
				var st = '<p>Error : ' + err.message + '</p>'
				return st
			});
			var similarBooks = data.map(similarB => {
				temp = []
				for (x = 0; x < similarB.similar_books.length; x++) {
					temp.push(`<p>similar_book : ` + similarB.similar_books[x]  + `</p>`)
				}
                return temp
            });
			html = data.map(book => {
				var s = '<p>book_url : ' + book.book_url + '</p>'
				+ '<p>title : ' + book.title + '</p>'
				+ '<p>book_id : ' + book.book_id + '</p>'
				+ '<p>ISBN : ' + book.ISBN + '</p>'
				+ '<p>author_url : ' + book.author_url + '</p>'
				+ '<p>author : ' + book.author + '</p>'
				+ '<p>rating : ' + book.rating + '</p>'
				+ '<p>rating_count : ' + book.rating_count + '</p>'
				+ '<p>review_count : ' + book.review_count + '</p>'
				+ '<p>image_url : ' + book.image_url + '</p>'
				+ '<p>book_id : ' + book.book_id + '</p>';
				return s + temp;
			});
			document.querySelector('#app').insertAdjacentHTML('afterbegin', html);
		}).catch(error=> {
			console.log(error);
		});	
}

function handleGetAuthor(authorID) {
	fetch("http://127.0.0.1:5000/author?id="+authorID)
		.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
			console.log(data);
			var relatedAuthors = data.map(relatedA => {
				temp = []
				for (x = 0; x < relatedA.related_authors.length; x++) {
					temp.push(`<p>related_author : ` + relatedA.related_authors[x]  + `</p>`)
				}
                return temp
            });
            var authorBooks = data.map(authorsB => {
				tmp = []
				for (x = 0; x < authorsB.author_books.length; x++) {
					tmp.push(`<p>author_book : ` + authorsB.author_books[x]  + `</p>`)
				}
                return tmp
            });
			const html = data.map(author => {
				var str = '<p>name : ' + author.name + '</p>'
                	+ '<p>author_url : '  + author.author_url  + '</p>'
                    + '<p>author_id : ' + author.author_id  + '</p>'
                    + '<p>image_url : ' + author.image_url  + '</p>'
                    + '<p>rating : ' + author.rating  + '</p>'
                    + '<p>rating_count : ' + author.rating_count  + '</p>'
                    + '<p>review_count : ' + author.review_count  + '</p>';
					return str + temp + tmp;
			});
			console.log(html)
			document.querySelector('#app').insertAdjacentHTML('afterbegin', html);
		}).catch(error=> {
			console.log(error);
		});	
}

function handleGetQuery(querystring) {
	var u = "http://127.0.0.1:5000/search?q=" + querystring
	console.log(u)
	fetch(u)
		.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
			console.log(data);
			if (querystring.includes('book')) {
				var similarBooks = data.map(similarB => {
					temp = []
					for (x = 0; x < similarB.similar_books.length; x++) {
						temp.push(`<p>similar_book : ` + similarB.similar_books[x]  + `</p>`)
					}
	                return temp
	            });
				const html = data.map(book => {
					var s = '<p>book_url : ' + book.book_url + '</p>'
					+ '<p>title : ' + book.title + '</p>'
					+ '<p>book_id : ' + book.book_id + '</p>'
					+ '<p>ISBN : ' + book.ISBN + '</p>'
					+ '<p>author_url : ' + book.author_url + '</p>'
					+ '<p>author : ' + book.author + '</p>'
					+ '<p>rating : ' + book.rating + '</p>'
					+ '<p>rating_count : ' + book.rating_count + '</p>'
					+ '<p>review_count : ' + book.review_count + '</p>'
					+ '<p>image_url : ' + book.image_url + '</p>'
					+ '<p>book_id : ' + book.book_id + '</p>';
					return s + temp;
				});
				console.log(html)
				document.querySelector('#app').insertAdjacentHTML('afterbegin', html);
			} else if (querystring.includes('author')) {
				var relatedAuthors = data.map(relatedA => {
					temp = []
					for (x = 0; x < relatedA.related_authors.length; x++) {
						temp.push(`<p>related_author : ` + relatedA.related_authors[x]  + `</p>`)
					}
	                return temp
	            });
	            var authorBooks = data.map(authorsB => {
					tmp = []
					for (x = 0; x < authorsB.author_books.length; x++) {
						tmp.push(`<p>author_book : ` + authorsB.author_books[x]  + `</p>`)
					}
	                return tmp
	            });
				const html = data.map(author => {
					var str = '<p>name : ' + author.name + '</p>'
	                	+ '<p>author_url : '  + author.author_url  + '</p>'
	                    + '<p>author_id : ' + author.author_id  + '</p>'
	                    + '<p>image_url : ' + author.image_url  + '</p>'
	                    + '<p>rating : ' + author.rating  + '</p>'
	                    + '<p>rating_count : ' + author.rating_count  + '</p>'
	                    + '<p>review_count : ' + author.review_count  + '</p>';
						return str + temp + tmp;
				});
				console.log(html)
				document.querySelector('#app').insertAdjacentHTML('afterbegin', html);
			}
			
			}).catch(error=> {
				console.log(error);
			});	
}

function handlePutBook(bookID, inp) {
	var u = "http://127.0.0.1:5000/book?id=" + bookID
	console.log(inp)
	console.log(u)
	var s = JSON.parse(inp)
	const putMethod = {
		method : "PUT",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, putMethod)
	.then(response => response.json())
	.then(data => console.log(data))
	.catch(error => console.log(error))
}

function handlePutAuthor(authorID, inp) {
	var u = "http://127.0.0.1:5000/author?id=" + authorID
	console.log(inp)
	console.log(u)
	var s = JSON.parse(inp)
	const putMethod = {
		method : "PUT",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, putMethod)
	.then(response => response.json())
	.then(data => console.log(data))
	.catch(error => console.log(error))
}

function handlePostBook(inp) {
	var u = "http://127.0.0.1:5000/books"
	console.log(inp)
	var s = JSON.parse(inp)
	const postMethod = {
		method : "POST",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, postMethod)
	.then(response => response.json())
	.then(data => console.log(data))
	.catch(error => console.log(error))
}

function handlePostAuthor(inp) {
	var u = "http://127.0.0.1:5000/authors"
	console.log(inp)
	var s = JSON.parse(inp)
	const postMethod = {
		method : "POST",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, postMethod)
	.then(response => response.json())
	.then(data => console.log(data))
	.catch(error => console.log(error))
}

function handleDeleteBook(bookID) {
	var u = "http://127.0.0.1:5000/book?id=" + bookID
	console.log(u)
	const deleteMethod = {
		method : "DELETE",
	}
	fetch(u, deleteMethod)
	.then(res => res.text())
	.then(res => console.log(res))
}
function handleDeleteAuthor(authorID) {
	var u = "http://127.0.0.1:5000/author?id=" + authorID
	console.log(u)
	const deleteMethod = {
		method : "DELETE",
	}
	fetch(u, deleteMethod)
	.then(res => res.text())
	.then(res => console.log(res))
}
