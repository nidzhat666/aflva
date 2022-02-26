export const userService = {
    userLogin,
};

async function userLogin(data) {
    let form_data = new FormData()
    for (let i in data) {
        form_data.append(i, data[i])
    }
    let token = await fetch('http://nzmaslo.ru:8080/api-token-auth/', {
        method: 'POST',
        body: form_data
    }).then((response) => {
        if (response.ok) {
            return response.json().then((json) => {
                return json
            })
        } else {
            throw 'Wrong username or password'
        }
    })
    let user = await fetch('http://nzmaslo.ru:8080/api-user/', {
        method: 'GET',
        headers: {Authorization: `Token ${token.token}`}
    }).then((response) => {
        if (response.ok) {
            return response.json().then((json) => {
                return json
            })
        } else {
            throw 'Wrong email or password'
        }
    })
    return Object.assign(user, token, {'status':'success'})
}
