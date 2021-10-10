function handleGetBook(bookID) {
	var u = "http://127.0.0.1:5000/book?id=" +bookID
	console.log(u)
	fetch(u)
		.then(response => {
		console.log(response)
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
    		console.log(data)
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
		
			document.querySelector('#app').insertAdjacentHTML('afterbegin', html);
		}).catch(error=> {
			const returnObject = '<p>Error: ' + 'Not a valid book' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
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
			const returnObject = '<p>Error: ' + 'Not a valid author' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
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
				const returnObject = '<p>Error: ' + 'Not a valid query' + '</p>'
				document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
			});	
}

function handlePutBook(bookID, inp) {
	var u = "http://127.0.0.1:5000/book?id=" + bookID
	console.log(inp)
	try {
		var s = JSON.parse(inp)
	} catch (err) {
		const returnObject = '<p>PUT Failed: ' + 'Book PUT request Failed' + '</p>'
		document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
		return;
	}
	const putMethod = {
		method : "PUT",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, putMethod)
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		}).then(data=> {
			const success = data.map(message => {
				var s = '<p>PUT Book Successful </p>'
				return s;
			});
			document.querySelector('#app').insertAdjacentHTML('afterbegin', success)
		})
		.catch(error => {
			if (error instanceof(SyntaxError)) {
				var s = '<p>PUT Book Successful </p>'
				return document.querySelector('#app').insertAdjacentHTML('afterbegin', s)
			} else {
				const returnObject = '<p>PUT Failed: ' + 'Book PUTT request Failed' + '</p>'
				document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
			}
		});
}

function handlePutAuthor(authorID, inp) {
	var u = "http://127.0.0.1:5000/author?id=" + authorID
	console.log(inp)
	try {
		var s = JSON.parse(inp)
	} catch {
		const returnObject = '<p>PUT Failed: ' + 'Author PUT request Failed' + '</p>'
		document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
		return;
	}
	const putMethod = {
		method : "PUT",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, putMethod)
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		}).then(data=> {
			
			var s = '<p>PUT Author Successful </p>'
			return s;
			document.querySelector('#app').insertAdjacentHTML('afterbegin', success)
		})
		.catch(error => {const returnObject = '<p>PUT Failed: ' + 'Author PUT request Failed' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
	});
}

function handlePostBook(inp) {
	var u = "http://127.0.0.1:5000/books"
	console.log(inp)
	try {
		var s = JSON.parse(inp)
	} catch {
		const returnObject = '<p>POST Failed: ' + 'Author POST request Failed' + '</p>'
		document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
		return;
	}
	const postMethod = {
		method : "POST",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, postMethod)
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		}).then(data=> {
			const success = data.map(message => {
				var s = '<p>POST Book Successful </p>'
				return s;
			});
			document.querySelector('#app').insertAdjacentHTML('afterbegin', success)
		})
		.catch(error => {const returnObject = '<p>POST Failed: ' + 'Book POST request Failed' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
	});
}

function handlePostAuthor(inp) {
	var u = "http://127.0.0.1:5000/authors"
	console.log(inp)
	try {
		var s = JSON.parse(inp)
	} catch {
		const returnObject = '<p>POST Failed: ' + 'Author POST request Failed' + '</p>'
		document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
		return;
	}
	
	const postMethod = {
		method : "POST",
		headers: {
			'Content-Type':'application/json'
		},
		body: JSON.stringify(s)
	}
	fetch(u, postMethod)
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		}).then(data=> {
			const success = data.map(message => {
				var s = '<p>POST Author Successful </p>'
				return s;
			});
			document.querySelector('#app').insertAdjacentHTML('afterbegin', success)
		})
		.catch(error => {const returnObject = '<p>POST Failed: ' + 'Author POST request Failed' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
	});
}

function handleDeleteBook(bookID) {
	var u = "http://127.0.0.1:5000/book?id=" + bookID
	console.log(u)
	const deleteMethod = {
		method : "DELETE",
	}
	fetch(u, deleteMethod)
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		}).then(data=> {
			const success = data.map(message => {
				var s = '<p>Delete Book Failed: ' + message.message + '</p>'
				return s;
			});
			document.querySelector('#app').insertAdjacentHTML('afterbegin', success)
		})
		.catch(error => {const returnObject = '<p>Success: ' + 'Book Delete request Successful' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
	});
}

function handleDeleteAuthor(authorID) {
	var u = "http://127.0.0.1:5000/author?id=" + authorID
	console.log(u)
	const deleteMethod = {
		method : "DELETE",
	}
	fetch(u, deleteMethod)
	.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
		}).then(data=> {
			const success = data.map(message => {
				var s = '<p>Delete Author Failed: ' + message.message + '</p>'
				return s;
			});
			document.querySelector('#app').insertAdjacentHTML('afterbegin', success)
		})
		.catch(error => {const returnObject = '<p>Success: ' + 'Author Delete request Successful' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
	});
}