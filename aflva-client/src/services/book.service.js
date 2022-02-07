export const bookService = {
    getAllBooks,
}
async function getAllBooks (token){
    return await fetch('https://afl-va.ru/api-book/',{
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
