var bolin_pages = ["002238", "002544", "002551", "002722", "002730", "002733", "002880", "002926", "002970", "003620"]
var bolhq_pages = ["002544", "002551", "002733", "002880", "002926", "002970"]

var looping_flashes = ['00980_1',]

module.exports = {
    hidden: true,
    
    edit(archive) {
        var hq_enabled = Boolean(archive.flags['HQAUDIO'])
        console.log("Setting Bolin audio", "hq=", hq_enabled)
        bolin_pages.forEach(page_num => {
            const page = archive.mspa.story[page_num]

            const filename = page.media[0].split('/').pop()
            const plainname = filename.split(".").slice(0, -1).join(".")
            const base_url = page.media[0].split("/").slice(0, -1).join("/")
            const ext = filename.split('.').pop()

            archive.mspa.story[page_num].media[0] = `${base_url}/${plainname}_bolin.${ext}`
            
            if (hq_enabled && bolhq_pages.includes(page_num)) {
                if (page_num == "002880") {
                    archive.audioData[page.media[0]] = [
                        {
                            href: `${base_url}/${plainname}_bolin_1.mp3`,
                            loop: (looping_flashes.includes(`${plainname}_1`))
                        },
                    ]
                } else {
                    archive.audioData[page.media[0]] = [
                        {
                            href: `${base_url}/${plainname}_bolin.mp3`,
                            loop: (looping_flashes.includes(plainname))
                        },
                    ]
                }
            }
        })
    }
}