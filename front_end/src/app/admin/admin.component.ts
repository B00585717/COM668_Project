import {Component} from "@angular/core";
import {WebService} from "../web.service";
import {FormGroup, FormControl, Validators, FormBuilder} from '@angular/forms';
import { ActivatedRoute } from "@angular/router";
import {VoteService} from "../vote.service";
import { AuthService } from '../auth.service';

@Component({
  selector: 'admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})

export class AdminComponent {

  formGroup: any;
  candidate_list: any = [];
  voter_list: any = [];
  party_list: any = [];




  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder, private voteService: VoteService, private authService: AuthService) {

  }

  ngOnInit() {

    this.formGroup = new FormGroup({
      candidate_firstname: new FormControl('', Validators.required),
      candidate_lastname: new FormControl('', Validators.required),
      party_id: new FormControl('', Validators.required),
      image: new FormControl('', Validators.required),
      constituency_id: new FormControl('', Validators.required),
      statement: new FormControl('', Validators.required)
    });

    this.candidate_list = this.webService.getCandidates();
    this.voter_list = this.webService.getUsers();
    this.party_list = this.webService.getParties();
  }


  onSubmit(candidateData: any, candidate: any) {
  this.webService.updateCandidate({...candidateData, candidate_id: candidate.candidate_id}).subscribe(
    response => {
      console.log('Candidate updated successfully', response);
      // You can refresh the candidate list here or show a success message
    },
    error => {
      console.error('Error updating candidate', error);
    }
  );
  }
  createForm(candidate: any) {
    this.formGroup = new FormGroup({
      candidate_firstname: new FormControl(candidate.candidate_firstname, Validators.required),
      candidate_lastname: new FormControl(candidate.candidate_lastname, Validators.required),
      party_id: new FormControl(candidate.party_id, Validators.required),
      image: new FormControl(candidate.image, Validators.required),
      constituency_id: new FormControl(candidate.constituency_id, Validators.required),
      statement: new FormControl(candidate.statement, Validators.required)
    });
  }
}
