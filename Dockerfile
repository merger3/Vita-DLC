FROM archlinux:latest as build

WORKDIR /root/torrents
ENV HOME=/root/torrents
ENV PATH="${PATH}:/root/torrents/bin"

RUN pacman -Syy  --noconfirm \
    coreutils \
    linux-headers \
	wget \
	bash \
	python \
	python-pip \
	curl \
	git \
	file \
	sed \
	grep \
	gcc \
	make \
	which


RUN mkdir bin
COPY PSV_DLCS.tsv .
COPY PSV_DLCS.tsv .
COPY PSV_GAMES.tsv .

RUN git clone https://github.com/Rudde/mktorrent.git
WORKDIR /root/torrents/mktorrent
RUN PREFIX=$HOME make
RUN PREFIX="${HOME}" make install

WORKDIR /root/torrents
RUN rm -rf ~/mktorrent

RUN git clone https://github.com/BubblesInTheTub/torrent7z.git
WORKDIR /root/torrents/torrent7z/linux_src/p7zip_4.65/
RUN make
RUN install -Dm 0755 bin/t7z "${HOME}/bin"

WORKDIR /root/torrents
RUN git clone https://github.com/lusid1/pkg2zip.git
WORKDIR /root/torrents/pkg2zip
RUN make
RUN install -D -m 0755 pkg2zip /root/torrents/bin/pkg2zip
RUN install -D -m 0755 rif2zrif.py /root/torrents/bin/rif2zrif
RUN install -D -m 0755 zrif2rif.py /root/torrents/bin/zrif2rif

WORKDIR /root/torrents
RUN git clone https://github.com/sigmaboy/nopaystation_scripts.git && cd nopaystation_scripts
WORKDIR /root/torrents/nopaystation_scripts
# RUN sed -i 's/MY_BINARIES="pkg2zip sed grep t7z file"/MY_BINARIES="sed grep t7z file"/' nps_dlc.sh
RUN chmod +x nps_*.sh pyNPU.py
RUN test -d "${HOME}/bin" && ln -s "$(pwd)"/nps_*.sh "$(pwd)"/pyNPU.py "${HOME}/bin"

# WORKDIR /root/torrents/bin
# COPY t7z .
# COPY mktorrent .
# COPY pkg2zip .

WORKDIR /root/torrents

RUN pip install torf


# RUN chmod -R 777 /root
# RUN chown -R 1000:1000 /root
COPY createTorrents.py .
# ENTRYPOINT ["tail", "-f", "/dev/null"]

ENTRYPOINT ["python3", "createTorrents.py"]