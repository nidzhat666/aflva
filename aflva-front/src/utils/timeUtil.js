export function secToHours(seconds){
    return Math.floor(seconds/3600)
}

export function secFormat(totalSeconds){
    let hours = Math.floor(totalSeconds / 3600);
    totalSeconds %= 3600;
    let minutes = Math.floor(totalSeconds / 60);
    let seconds = totalSeconds % 60;
    return hours + ":" + minutes + ":" + seconds
}
