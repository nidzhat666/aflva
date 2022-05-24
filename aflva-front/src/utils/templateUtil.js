import {Tooltip} from 'bootstrap'

export function tooltipUpdate(){
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    tooltipTriggerList.forEach(element => {
        new Tooltip()
        new Tooltip(element, {container: 'body'})
    })
}
