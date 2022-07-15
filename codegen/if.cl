class Main inherits IO {
    main(): Object {
        let cond: Bool <- false
        in {
            if cond
            then out_int(1)
	    	else out_int(2)
	    	fi;
        }
    };
};