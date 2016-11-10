def packages(options,front,data_f,data_h,av):

    result_list = []
    for i in range(len(front)):
        for option in options:

            if int(option['key']) == int(front[i]):
                result_list.append(option['name'])
    print(result_list)
    print(data_f)
    print(data_h)
    results=[]
    for k in range(len(result_list)):
        a=result_list[k].split(',')
        flight=int(a[0][-1:])
        hotel=int(a[1][-1:])
        f=data_f[flight-1]
        h=data_h[hotel-1]
        hotel_package={a[1]:h}
        package = f.copy()
        package.update(hotel_package)
        all = package.copy()
        all.update(av)
        results.append(all)

    return(results)




