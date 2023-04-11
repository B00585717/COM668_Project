import {Component} from "@angular/core";
import {FormBuilder} from "@angular/forms";
import {ActivatedRoute} from "@angular/router";
import {WebService} from "../services/web.service";

@Component({
  selector: 'candidate',
  templateUrl: './candidate.component.html',
  styleUrls: ['./candidate.component.css']
})

export class CandidateComponent {

  candidate: any;


  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {
  }

ngOnInit() {
  this.webService.getCandidate(this.route.snapshot.params['id']).subscribe(
    (candidateData: any) => {
      console.log("Candidate data received:", candidateData);
      this.candidate = candidateData[0];
    },
    (error) => {
      console.error("Error fetching candidate data:", error);
    }
  );
}
}
