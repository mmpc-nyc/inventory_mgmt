export default function authHeader() {
    let user = JSON.parse(localStorage.getItem('user'));

    if (user && user.access) {
        return {
            'Authorization': "JWT " + user.access,
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
            ;
    } else {
        return {};
    }
}


