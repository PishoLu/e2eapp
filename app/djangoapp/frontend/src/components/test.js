a = [{
    id: 1,
    message: "{'id':'1.1'}"
}, {
    id: 2,
    message: "{'id':'2.1'}"
}]
b = []
Promise.all(a.map(item => {
    if (b.indexOf(item["id"]) === -1) {
        b.push(item["id"])
    }
})).then(res => {
    b.map(item => {
        setTimeout(() => {
            console.log(item)
        }, 2000);
    })
    console.log("OK")
})