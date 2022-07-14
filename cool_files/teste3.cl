class Main inherits IO {
    init(map : String) : String {
      (let x : Int <- 1 in
         {
            (new E).set_var(x);
         }
      )
    };
    population_map : String <- "a";
};


