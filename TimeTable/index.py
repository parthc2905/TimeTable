import random
import numpy as np

def tableGen(numberOfDays,numOflecure,numofsub,breaktime,namefaculty,nameSubject,lectureduraion,numofdiv):
    
    # Number of days per week       
    # total_days_per_week = int(input("Enter for how many days per week: "))
    total_days_per_week = numberOfDays

    # Number of hours(in min) of the lectures in total per day 
    # total_time = int(input("Total Time of lectures per day (in min): "))
    total_time = lectureduraion*numOflecure

    # Per lecture Duration
    # lecture_duration = int(input("Enter Time per lecture(in min): "))
    lecture_duration = lectureduraion

    # Break time
    # break_time = int(input("Enter break times (in min): "))
    break_time = breaktime

    # Making time block for each day
    time_block = ((total_time//lecture_duration)//2)*[lecture_duration] + [break_time] + ((total_time//lecture_duration)//2)*[lecture_duration]

    # subjects 
    subjects = nameSubject
    # Taking information about the faculties and their subjects
    # for i in range(enter_number_of_faculty):
    #     name = input( f"Enter name of faculty {i+1}(in short form) : ")
    #     subject = input(f"Subject taught buy {i+1} faculty : ")
    #     names.append(name)
    #     subjects.append(subject)

    #How many divisions
    # number_of_division = int(input("Enter number of division to make the time Table : "))
    number_of_division = numofdiv
    
    

    # Generates Time Table
    division = {}
    i = 1
    while 0<number_of_division:
        subject_block = [] 
        # subject block for each day assigned

        # creates block for each day
        for day in range(total_days_per_week):
            temp = subjects.copy()
            subject_per_day = []
            for lecture in range(total_time//lecture_duration + 1 ):
                rand = random.choice(temp)
                if lecture == (total_time//lecture_duration)//2:
                    subject_per_day.append("Break")
                else:
                    temp.remove(rand)
                    subject_per_day.append(rand)
        
            subject_block.append(subject_per_day)

        division[i] = subject_block
        i+=1
        # start printing table
        # print("\nTime ", *days[:total_days_per_week])

        # printing Each block
        # for lecture in range(total_time//lecture_duration+1):
        #     print(f" {time_block[lecture]} ",end=" ")
        #     for day in range(total_days_per_week):
        #         print(f" {subject_block[day][lecture]} ", end=" ")
        #     print()
        # print()
        number_of_division -= 1

    # print(division,time_block)
    # for i in range(len(division)):
    #     df = pd.DataFrame(division[i+1])
    #     df.to_csv(f't{i+1}.csv',index=False) 
    
    available_subjects = nameSubject

    # Convert each division's schedule to a NumPy array for processing.
    # We'll sort divisions by key to have a consistent order.
    div_keys = sorted(division.keys())
    schedules_np = [np.array(division[k]) for k in div_keys]

    # Determine number of days and slots (assuming all divisions have the same shape)
    num_divisions = len(schedules_np)
    num_days, num_slots = schedules_np[0].shape

    # Identify and resolve conflicts across divisions for each day and slot.
    # Conflict: same subject (not "Break") appears in the same slot across divisions.
    for day in range(num_days):
        for slot in range(num_slots):
            # Gather subjects for current day and slot from all divisions
            subjects_in_slot = [schedules_np[i][day, slot] for i in range(num_divisions)]
            
            # Process only if the subject is not "Break"
            if "Break" in subjects_in_slot:
                continue  # Skip this slot if it contains "Break"
            
            # If duplicates exist, resolve the conflict.
            # We'll keep the first occurrence and change duplicates.
            seen_subjects = set()
            for i in range(num_divisions):
                subject = schedules_np[i][day, slot]
                if subject in seen_subjects:
                    # Choose a new subject that is not already used in this slot.
                    # We check against subjects already present (seen_subjects)
                    new_options = [s for s in available_subjects if s not in seen_subjects]
                    if new_options:
                        new_subject = random.choice(new_options)
                        schedules_np[i][day, slot] = new_subject
                        seen_subjects.add(new_subject)
                    else:
                        # If no new option is available, keep the subject as is.
                        pass
                else:
                    seen_subjects.add(subject)

    # Convert the resolved NumPy arrays back to the original dictionary structure
    resolved_division = {}
    for idx, key in enumerate(div_keys):
        # Convert NumPy array to list of lists
        resolved_division[key] = schedules_np[idx].tolist()

    # Build the final output dictionary
    return (resolved_division,total_days_per_week,total_time//lecture_duration+1,time_block)