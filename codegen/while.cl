class Main inherits IO {
    main(): Object {
        let cond: Bool <- true, outro: Bool <- false
        in {
            while cond loop
                {
                    out_int(5);
                    if outro then {
                        cond <- false;
                    }
                    else {
                        outro <- true;
                    }
                    fi;
                }
            pool;
        }
    };
};