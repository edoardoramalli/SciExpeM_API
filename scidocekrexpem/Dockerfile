FROM continuumio/miniconda3

LABEL Timoteo Dinelli "timoteo.dinelli@polimi.it", Edoardo Ramalli "edoardo.ramalli@polimi.it"

RUN useradd -ms /bin/bash sciexpem && echo "sciexpem:sciexpem" | chpasswd && adduser sciexpem sudo

USER root
RUN apt-get -y update && \
    apt-get install -y \
    g++ \
    gcc \
    git \
    vim \
    bash-completion \
    sudo \
    nano \
    wget

RUN chown -R sciexpem:sciexpem /home/sciexpem

USER sciexpem

WORKDIR /home/sciexpem
RUN mkdir /home/sciexpem/GitHub && mkdir /home/sciexpem/worker
RUN cd /home/sciexpem/GitHub && \
	git clone https://github.com/edoardoramalli/SciExpeM_API.git && \
	git clone https://github.com/edoardoramalli/sciexpem.git && \
	git clone https://github.com/acuoci/OpenSMOKEppTutorials.git
RUN cp -r /home/sciexpem/GitHub/sciexpem/SciExpeMWorker/* /home/sciexpem/worker

USER sciexpem

COPY environment.yml /home/sciexpem/

RUN echo "\n#~~~\n# My Settings\n#~~~\n\n" >> ~/.bashrc && \
   echo "PS1='\[\e[1;32m\]\u@\h:\[\e[1;34m\]\w\[\e[m\] \[\e[1;32m\]\$\[\e[m\] '" >> ~/.bashrc && \
   echo "shopt -s direxpand\n" >> ~/.bashrc && \
   . ~/.bashrc

SHELL ["/bin/bash", "-c"]

RUN conda env create -f environment.yml
RUN conda init bash
RUN echo "conda activate $(head -1 /home/sciexpem/environment.yml | cut -d' ' -f2)" >> ~/.bashrc
ENV PATH /home/sciexpem/.conda/envs/$(head -1 /home/sciexpem/environment.yml | cut -d' ' -f2)/bin:$PATH
ENV CONDA_DEFAULT_ENV $(head -1 /home/sciexpem/environment.yml | cut -d' ' -f2)

CMD /bin/bash
