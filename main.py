import sys, glob, subprocess, os, time


#assume top_dir ends in /
#returns a list of filepaths of video files that haven't been encoded before
def find_video_files(top_dir : str) -> list:
    #searches for avi/mpg/mov/mp4 files
    file_list = glob.glob(f'{top_dir}**/*.[aA][vV][iI]', recursive=True)
    file_list.extend(glob.glob(f'{top_dir}**/*.[mM][pP][gG]', recursive=True))
    file_list.extend(glob.glob(f'{top_dir}**/*.[mM][oO][vV]', recursive=True))
    file_list.extend(glob.glob(f'{top_dir}**/*.[mM][pP]4', recursive=True))
    #check for previously completed jobs
    
    if not os.path.exists("completed_log.txt"):
        open("completed_log.txt", "w").close() #if it doesn't exist, create a new one
    completed_log = open("completed_log.txt", "r")
    log_data = completed_log.read()
    checked_list = []
    for x in file_list:
        if x not in log_data:
            checked_list.append(x)
    return checked_list


#doesn't save completed files in log if exited with ctrl-c... I think
def call_handbrake(file_dirs : list, num_files : int):
    hb_command = "flatpak run --command=HandBrakeCLI fr.handbrake.ghb"
    command_args = '-Z "Fast 1080p30"'
    #initializing just in case
    command_file_source = ""
    command_file_destination = ""
    is_mp4 = False
    i, j = (1, len(file_dirs))
    completed_log = open("completed_log.txt", "a")
    for x in file_dirs:
        command_file_source = x
        if os.path.splitext(command_file_source)[1].lower() != '.mp4':
            #if not mp4, write as mp4
            command_file_destination = f"{command_file_source.replace(command_file_source.split('.')[-1], 'mp4')}"
            is_mp4 = False
        else: 
            #if mp4, add underscore to diferentiate from the source file
            #(it is then renamed back to .mp4 after the encode is done and the original is deleted)
            command_file_destination = f"{command_file_source.replace('.mp4', '_.mp4')}"
            is_mp4 = True
        #'File (current) of (max/total), depending on the number argument
        print(f'File {i} of {num_files if num_files != -1 else j} ({j} total) ...')
        print(f'Encoding "{command_file_source}" into "{command_file_destination}"...')
        output = subprocess.run(f"""{hb_command} -i "{command_file_source}" -o "{command_file_destination}" {command_args}""", shell=True, capture_output=True, text=True)
        if "Encode done" in output.stderr:
            print('Encode successful')
        else:
            print('Problem while encoding?')
            print(f'Output: \n {output.stderr}') #check output for encoding problems
            print('Likely a broken video file, aborting just in case...')
            break
        print(f"Deleting original video file {command_file_source}...")

        #bunch of debugging prints here to figure out why the 'file not found' error occurs when renaming
        #I suspect it happens when the encode fails above, but to be sure...
        if os.path.exists(command_file_source):
            print(f'Original file {command_file_source} exists')
            os.remove(command_file_source)
        else:
            print('Original file does not exist. File not deleted.')
        if is_mp4:
            print("Renaming exported file to the original file's name...")
            fname = command_file_destination.replace('_.', '.')
            if os.path.exists(fname):
                raise Exception(f'Renamed file destination {fname} exists, should have been deleted. Aborting.')
            elif os.path.exists(command_file_destination):
                print(f'_ file destination {command_file_destination} exists, attempting rename...')
                os.rename(command_file_destination, fname)
                completed_log.write(f'{fname}\n')
        else:
            completed_log.write(f'{command_file_destination}\n')    
        print("...done")
        print("---\n")
        i += 1  
  
        if num_files != -1 and i > num_files :
            print(f'Processed {num_files} files, exiting...')
            break
    completed_log.close()   
        
def do_the_thing():
    top_dir = sys.argv[1] #get directory
    number_to_process = int(sys.argv[2]) #get number of files to process
    video_files = find_video_files(top_dir)
    if not video_files: #if list is empty
        print("All files already processed")
    else:
        call_handbrake(video_files, number_to_process)

if __name__ == "__main__":
    do_the_thing()
