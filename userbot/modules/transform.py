# Authored by @Khrisna_Singhal
# Ported from Userge by Alfiananda P.A

import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageOps
from telethon.tl.types import DocumentAttributeFilename

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register

Converted = TEMP_DOWNLOAD_DIRECTORY + "sticker.webp"


@register(outgoing=True, pattern=r"^\.(mirror|flip|ghost|bw|poster)$")
async def transform(event):
    if not event.reply_to_msg_id:
        await event.edit("`Balas ke media apa saja..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`membalas gambar/stiker`")
        return
    await event.edit("`Mendownload Media..`")
    if reply_message.photo:
        transform = await bot.download_media(
            reply_message,
            "transform.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "transform.tgs",
        )
        os.system("lottie_convert.py transform.tgs transform.png")
        transform = "transform.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "transform.mp4",
        )
        extractMetadata(createParser(video))
        os.system(
            "ffmpeg -i transform.mp4 -vframes 1 -an -s 480x360 -ss 1 transform.png"
        )
        transform = "transform.png"
    else:
        transform = await bot.download_media(
            reply_message,
            "transform.png",
        )
    try:
        await event.edit("`Mentransformasi media ini..`")
        cmd = event.pattern_match.group(1)
        im = Image.open(transform).convert("RGB")
        if cmd == "mirror":
            IMG = ImageOps.mirror(im)
        elif cmd == "flip":
            IMG = ImageOps.flip(im)
        elif cmd == "ghost":
            IMG = ImageOps.invert(im)
        elif cmd == "bw":
            IMG = ImageOps.grayscale(im)
        elif cmd == "poster":
            IMG = ImageOps.posterize(im, 2)
        IMG.save(Converted, quality=95)
        await event.client.send_file(
            event.chat_id, Converted, reply_to=event.reply_to_msg_id
        )
        await event.delete()
        os.system("rm *.mp4 *.tgs")
        os.remove(transform)
        os.remove(Converted)
    except BaseException:
        return


@register(outgoing=True, pattern=r"^\.rotate(?: |$)(.*)")
async def rotate(event):
    if not event.reply_to_msg_id:
        await event.edit("`Balas media apa pun..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`membalas gambar/stiker`")
        return
    await event.edit("`Mendownload Media..`")
    if reply_message.photo:
        rotate = await bot.download_media(
            reply_message,
            "transform.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "transform.tgs",
        )
        os.system("lottie_convert.py transform.tgs transform.png")
        rotate = "transform.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "transform.mp4",
        )
        extractMetadata(createParser(video))
        os.system(
            "ffmpeg -i transform.mp4 -vframes 1 -an -s 480x360 -ss 1 transform.png"
        )
        rotate = "transform.png"
    else:
        rotate = await bot.download_media(
            reply_message,
            "transform.png",
        )
    try:
        value = int(event.pattern_match.group(1))
        if value > 360:
            raise ValueError
    except ValueError:
        value = 90
    await event.edit("`Memutar media Anda..`")
    im = Image.open(rotate).convert("RGB")
    IMG = im.rotate(value, expand=1)
    IMG.save(Converted, quality=95)
    await event.client.send_file(
        event.chat_id, Converted, reply_to=event.reply_to_msg_id
    )
    await event.delete()
    os.system("rm *.mp4 *.tgs")
    os.remove(rotate)
    os.remove(Converted)


CMD_HELP.update(
    {
        "transform": ">`.ghost`"
        "\nUsage: ubah foto teman  Anda menjadi hantu!."
        "\n\n>`.flip`"
        "\nUsage: Untuk membalik gambar Anda"
        "\n\n>`.mirror`"
        "\nUsage: Untuk membalikkan posisi media Anda"
        "\n\n>`.bw`"
        "\nUsage: Untuk mengubah gambar berwarna Anda menjadi gambar b/w!"
        "\n\n>`.poster`"
        "\nUsage: Untuk mem-poster gambar Anda!"
        "\n\n>`.rotate <value>`"
        "\nUsage: Untuk memutar gambar Anda\n* Nilainya berkisar 1-360 jika tidak akan memberikan nilai default yaitu 90"
    }
)
