import {Modal} from 'bootstrap'

export default () => {
    console.log('hello world')
    const myModal = new Modal('#bookModal', {
        keyboard: true
    })
    myModal.show()
}
