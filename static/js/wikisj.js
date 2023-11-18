/* ---- 项目存活时间 ---- */

function getTimeDifference(startTime) {
    // 将开始时间和当前时间都转换为时间戳
    const startTimestamp = new Date(startTime).getTime();
    const currentTimestamp = new Date().getTime();

    // 计算时间差（单位：毫秒）
    const timeDifference = currentTimestamp - startTimestamp;

    // 计算天数、小时数、分钟数和秒数
    const days = Math.floor(timeDifference / (24 * 60 * 60 * 1000));
    const hours = Math.floor((timeDifference % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000));
    const minutes = Math.floor((timeDifference % (60 * 60 * 1000)) / (60 * 1000));
    const seconds = Math.floor((timeDifference % (60 * 1000)) / 1000);

    return {
        days,
        hours,
        minutes,
        seconds
    };
}

function siteTime() {
    window.setTimeout("siteTime()", 1000);
    // 指定开始时间（格式为YYYY-MM-DDTHH:mm:ss）
    const startTime = "2023-11-17T00:00:00";
    // 获取时间差
    const timeDifference = getTimeDifference(startTime);

    document.getElementById("sitetime").innerHTML = "<span>"
        + timeDifference.days + "</span> 天 <span>"
        + timeDifference.hours + "</span> 小时 <span>"
        + timeDifference.minutes + "</span> 分钟 <span>"
        + timeDifference.seconds + "</span> 秒"
}

siteTime()
