
function searchfind (){
    var form = new FormData();
    var files = document.getElementById("file").files;
    var file = files[0];
    form.append("file", file, file.name);
                $.ajax({
                url: "/hello",
                method: "POST",
                processData: false,
                mimeType: "multipart/form-data",
                contentType: false,
                data: form,
                statusCode: {
                404: function(responseObject, textStatus, jqXHR) {
                    alert('not found');
                    // No content found (404)
                    // This code will be executed if the server returns a 404 response
                },
                400: function(responseObject, textStatus, jqXHR) {
                    alert('Bad Request');
                    // No content found (404)
                    // This code will be executed if the server returns a 404 response
                },
                403: function(responseObject, textStatus, jqXHR) {
                    alert('Forbidden');
                    // No content found (404)
                    // This code will be executed if the server returns a 404 response
                },
                500: function(responseObject, textStatus, jqXHR) {
                    alert('Server Error');
                    // No content found (404)
                    // This code will be executed if the server returns a 404 response
                },
                503: function(responseObject, textStatus, errorThrown) {
                    alert("unavailable");
                    // Service Unavailable (503)
                    // This code will be executed if the server returns a 503 response
                }},
                success: function (data, statusCode){
                    alert(data)
                },
                async: false,
                cache: false,
                timeout: 100000           
            });
    }
