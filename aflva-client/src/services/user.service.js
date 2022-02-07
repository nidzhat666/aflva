export const userService = {
    userLogin,
};

async function userLogin(data) {
    let form_data = new FormData()
    for (let i in data) {
        form_data.append(i, data[i])
    }
    let token = await fetch('https://afl-va.ru/api-token-auth/', {
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
    let user = await fetch('https://afl-va.ru/api-user/', {
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
