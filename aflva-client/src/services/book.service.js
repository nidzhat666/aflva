export const bookService = {
    getAllBooks,
}
async function getAllBooks (token){
    return await fetch('http://nzmaslo.ru:8080/api-book/',{
        method:'GET',
        headers: {Authorization: `Token ${token}`}
    }).then(response=>{
        if(response.ok){
            return response.json().then(json=>{
                return json
            })
        }
    })
}
