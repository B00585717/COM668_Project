import {Component, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import Chart from 'chart.js/auto';

@Component({
  selector: 'voting-data',
  templateUrl: './voting-data.component.html',
  styleUrls: ['./voting-data.component.css']
})
export class VotingDataComponent implements OnInit {
  votingData: any[] = [];
  public votingPieChart: any;
  public votingBarChart: any;

  constructor(private webService: WebService) { }

  ngOnInit(): void {
    this.webService.getVotingData().subscribe((data: any) => {
      this.votingData = data;
      this.createPieChart()
      this.createBarChart()
      console.log(this.votingData)
    });
  }

  createPieChart(){
    const candidateNames = this.votingData.map(candidate => candidate.candidate_name);
    const colors = this.getColours(candidateNames.length);
      this.votingPieChart = new Chart("votingPieChart", {
        type: 'doughnut',

        data: {
          labels: candidateNames,
           datasets: [
            {
              label: "Vote Percentage",
              data: this.votingData.map(candidate => candidate.vote_percentage),
              backgroundColor: colors
            },
          ]
        },
        options: {
          aspectRatio:1
        }
      });
  }

  createBarChart(){
    const candidateNames = this.votingData.map(candidate => candidate.candidate_name);
    const colors = this.getColours(candidateNames.length);
      this.votingBarChart = new Chart("votingBarChart", {
        type: 'bar',

        data: {
          labels: candidateNames,
           datasets: [
            {
              label: "Vote Percentage",
              data: this.votingData.map(candidate => candidate.vote_percentage),
              backgroundColor: colors
            },
          ]
        },
        options: {
          aspectRatio:1
        }
      });
  }
  getColours(count: number) {
    return ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'black', 'lilac', 'gold'];
}

}
