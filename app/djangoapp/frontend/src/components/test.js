let a = Array(10)

async function wait(time) {
    await new Promise(resolve => setTimeout(resolve, time));
}
function test(a) {
    setTimeout(async () => {
        for (let i = 0; i < a.length; i++) {
            await wait(2000)
            console.log(i)
        }
    }, 2000);
}